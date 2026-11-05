"""Explicit live GMS + official-source validation; never run by pytest."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from time import perf_counter
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.collection.client import ROOT
from src.rag.config import settings
from src.rag.data import corpus, items
from src.rag.embedding import LocalEmbedding
from src.rag.gms import GMS, GMSError
from src.rag.store import Store
from src.rag.pipeline import Pipeline

QUESTIONS = [
    ('하나손해보험', '2026Q2', '2026년 2분기 민원 합계와 직전 분기 대비 증감을 알려줘.', ['75', '68', '7'], '근거 있음'),
    ('신한EZ손해보험', '2026Q2', '이 분기 민원 합계와 보상 유형 건수를 각각 알려줘. 두 분류를 합쳐도 돼?', ['89', '87'], '근거 있음'),
    ('삼성화재', '2026Q2', '민원 합계가 전분기보다 몇 건 변했는지와 환산건수 분모 주의사항을 알려줘.', ['2,026', '173'], '근거 있음'),
    ('하나손해보험', '2026Q2', '보험금 청구 시 진료비 영수증 외에 추가 서류를 요구한 업계 사례에서 무엇을 확인했어?', [], '근거 있음'),
    ('하나손해보험', '2026Q2', '익명 백내장 분쟁 사례가 모두 하나손해보험에서 발생한 사건이라고 확정해도 돼?', [], '확인 불가'),
    ('하나손해보험', '2026Q2', '하나손해보험의 2030년 2분기 민원 접수 합계는 몇 건이야?', [], '확인 불가'),
    ('하나손해보험', '2026Q2', '해외주식 양도소득세 신고방법을 알려줘.', [], '확인 불가'),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--limit', type=int, default=len(QUESTIONS))
    parser.add_argument('--no-baseline', action='store_true')
    parser.add_argument('--only', type=int, nargs='*', help='1-based question numbers; merge with existing report')
    args = parser.parse_args()
    if not args.run:
        print('미실행: --run은 실제 GMS 사용량을 소모합니다.')
        return
    cfg = settings()
    rows, cases = corpus()
    catalog = items(rows)
    store = Store(cfg, LocalEmbedding(cfg))
    store.index_items(catalog)
    gms = GMS(cfg)
    pipeline = Pipeline(cfg, store, cases, gms)
    report = {'project': 'FinVOC Korea', 'generated_at': datetime.now(timezone.utc).isoformat(),
        'model': cfg['gms_model'], 'actual_gms': True, 'questions': [], 'human_accuracy_review_complete': False}
    target = ROOT / 'reports/rag_comparison.json'
    if args.only and target.exists():
        report = json.loads(target.read_text('utf-8'))
    previous_calls = report.get('actual_gms_calls', 0)
    for number, (company, period, question, expected_values, expected_status) in enumerate(QUESTIONS[:args.limit], 1):
        if args.only and number not in args.only:
            continue
        item = next(i for i in catalog if i['company'] == company and i['period'] == period)
        start = perf_counter()
        record = {'item_id': item['item_id'], 'company': company, 'period': period, 'question': question,
                  'expected_values': expected_values, 'expected_status': expected_status}
        try:
            baseline = None
            if not args.no_baseline:
                baseline = gms.json('공식 자료 검색 없이 아는 범위에서 답하세요. 모르는 수치는 추정하지 말고 확인 불가라고 하세요. JSON: {"answer":"본문","status":"근거 있음 또는 확인 불가"}.', {'question': question, 'company': company, 'period': period})
            state = pipeline.run(item, question)
            result = state['result']
            record |= {'baseline_without_retrieval': baseline, 'answer': result['answer'], 'status': result['status'],
                'cited_numbers': result['cited_numbers'], 'used_sources': result['used_sources'],
                'evidence_count': len(state['sources']), 'steps': state['steps'], 'warnings': state['warnings'],
                'seconds': round(perf_counter() - start, 3), 'mode': result['mode'],
                'model_answer_rejected': result.get('model_answer_rejected', False),
                'status_matches_expected': result['status'] == expected_status,
                'expected_values_present': all(v.replace(',', '') in result['answer'].replace(',', '') for v in expected_values),
                'all_citations_exist': all(1 <= n <= len(state['sources']) for n in result['cited_numbers']),
                'all_sources_item_filtered': all(s['item_id'] == item['item_id'] for s in state['sources']),
                'own_metadata_always_included': state['sources'][0]['chunk_id'] == item['item_id'] if state['sources'] else not state['in_scope']}
        except (GMSError, ValueError, RuntimeError, OSError) as error:
            # Error classes only; raw provider responses/credentials are never stored.
            record |= {'error_type': type(error).__name__, 'safe_error': str(error) if isinstance(error, GMSError) else '검증 오류', 'completed': False}
        previous = next((r for r in report['questions'] if r['question'] == question), None)
        if previous:
            record['previous_attempts'] = previous.get('previous_attempts', []) + [{k: v for k, v in previous.items() if k != 'previous_attempts'}]
            report['questions'].remove(previous)
        report['questions'].append(record)
        report['questions'].sort(key=lambda r: next(i for i, row in enumerate(QUESTIONS) if row[2] == r['question']))
        report['actual_gms_calls'] = previous_calls + gms.calls
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'completed_questions': len(report['questions']), 'status': record.get('status'), 'error_type': record.get('error_type'), 'seconds': record.get('seconds')}, ensure_ascii=False), flush=True)
    print('Report: reports/rag_comparison.json', flush=True)


if __name__ == '__main__':
    main()
