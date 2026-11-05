"""캐시·본문·통계·인용을 실제 파일로 검사하고 Phase 0 판정의 근거를 남긴다."""
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from src.collection.client import Client, ROOT
from src.analysis.case_search import CaseSearch, validate_citation


def read(name):
    return json.loads((ROOT / name).read_text('utf-8'))


def main():
    sources = read('data/metadata/source_catalog.json')
    catalog = read('data/metadata/case_catalog.json')
    cases = read('data/private/cases.json')
    insurers = read('data/processed/insurer_stats.json')
    titles = defaultdict(list)
    for case in cases:
        titles[case['title']].append(case['case_id'])
    receipts = {r['document']['local_path']: r['document'] for r in sources}
    receipts.update({r['receipt']['local_path']: r['receipt'] for r in catalog})
    integrity = []
    for rel, receipt in receipts.items():
        path = ROOT / rel
        integrity.append({'path': rel, 'ok': path.is_file() and
                          hashlib.sha256(path.read_bytes()).hexdigest() == receipt['sha256']})
    # 재요청은 실제 운영 캐시로 실행한다. HTTP가 생기면 단순 캐시 성공으로 기록하지 않는다.
    client = Client()
    for receipt in receipts.values():
        client.fetch(receipt['url'], 'pdf' if receipt['local_path'].endswith('.pdf') else 'html')
    privacy_patterns = {
        'email': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        'phone': r'\b\d{2,3}-\d{3,4}-\d{4}\b',
        'resident_number_like': r'\b\d{6}-[1-4]\d{6}\b'}
    flags = {name: [c['case_id'] for c in cases if re.search(pattern, c['text'])]
             for name, pattern in privacy_patterns.items()}
    # 개발자가 원문을 보며 정한 작은 스모크 세트. 독립 정답셋/30문항 성능평가가 아니다.
    smoke = [
        ('백내장 다초점 인공수정체 수술 실손 보상', {'fss_case_71', 'fss_case_162'}),
        ('건강검진 의심소견 고지의무', {'fss_case_62'}),
        ('유니버셜 종신보험 해피콜 설명의무', {'fss_case_63'}),
        ('연금 가입설계서 예상 배당금', {'fss_case_130'}),
        ('청구서류 영수증 추가 진단서 제출', {'fss_case_73'})]
    search = CaseSearch(cases)
    checks = []
    for query, expected in smoke:
        hits = search.search(query, 5)
        checks.append({'query': query, 'expected_ids': sorted(expected),
                       'actual_ids': [h['case_id'] for h in hits],
                       'expected_in_top5': bool(expected.intersection(h['case_id'] for h in hits)),
                       'all_excerpt_citations_valid': all(validate_citation(
                           cases, h['case_id'], p['paragraph'], p['text']) for h in hits for p in h['excerpts'])})
    report = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'stage': 'Phase 0: 실제 데이터 확보·구조·검색 및 출처 검증',
        'sources': {'aggregate_documents': 2, 'insurers': sorted({r['company'] for r in insurers}),
                    'common_quarters': sorted(set.intersection(*[
                        {r['period'] for r in insurers if r['company'] == company}
                        for company in sorted({r['company'] for r in insurers})])),
                    'pdf_pages_extracted': sum(r['pages'] for r in read('reports/pdf_inventory.json'))},
        'cases': {'published_documents': len(cases), 'exact_unique_bodies': len({c['text_sha256'] for c in cases}),
                  'unique_titles': len(titles), 'unique_real_world_incidents': None,
                  'duplicate_title_groups': [ids for ids in titles.values() if len(ids) > 1],
                  'service_counts_of_published_documents': dict(Counter(c['service'].split('(')[0] for c in cases)),
                  'empty_fields': {field: sum(c[field] in {None, ''} for c in cases)
                                   for field in ['facts','issues','resolution_text','company_name','decision_date',
                                                 'consumer_argument','company_argument','reasoning','decision']},
                  'paragraphs': sum(len(c['paragraphs']) for c in cases),
                  'important': '처리결과에 판단 근거와 처리내용이 통합되어 있다. 분리된 결정주문/주장은 추정하지 않았다.'},
        'integrity': {'checked_files': len(integrity), 'passed': all(r['ok'] for r in integrity),
                      'failed_paths': [r['path'] for r in integrity if not r['ok']]},
        'cache_repeat': {'files_checked': len(receipts), 'cache_hits': client.hits, 'http_calls': client.calls},
        'privacy_pattern_flags': flags,
        'privacy_limit': '정규식 검사는 실명·간접 식별정보까지 없다는 보증이 아니다. 원문 공개 전 사람 검토 필요.',
        'search_smoke': {'method': '문자 2~4gram TF-IDF cosine', 'queries': checks,
                         'independent_evaluation': False, 'semantic_embedding_tested': False},
        'statistics': read('reports/statistics_validation.json'),
        'cross_source_checks': read('reports/cross_source_validation.json'),
        'technical_data_gate_passed': len(cases) >= 30 and all(c['facts'] and c['issues'] and c['resolution_text'] for c in cases)
                                      and all(r['ok'] for r in integrity)
                                      and all(c['expected_in_top5'] and c['all_excerpt_citations_valid'] for c in checks),
        'public_reuse_gate_passed': False,
        'public_reuse_reason': '금감원 원문 재배포/외부 사이트 게시 허락은 확인되지 않음. 교육·연구용 로컬 검토와 구분.',
        'not_yet_validated': ['30문항 독립 검색 정답셋', '한국어 의미 임베딩·ChromaDB', '실제 LLM 생성·인용 의미 일치',
                              '사람 검수한 민원유형 라벨', '공개 배포/원문 재배포 조건', '회사별 세부 제외 기준의 완전 일치']}
    (ROOT / 'reports/phase0_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'cases': len(cases), 'source_files_verified': len(integrity),
                      'repeat_http_calls': client.calls, 'technical_gate_passed': report['technical_data_gate_passed']},
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
