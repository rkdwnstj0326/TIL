"""출처의 실제 구획만 보존한다. 미공개 회사명·분리되지 않은 주장은 추정하지 않는다."""
import hashlib
import json
import re
from bs4 import BeautifulSoup, NavigableString
from src.collection.client import ROOT

HEADINGS = {'민원내용', '쟁점', '처리결과', '소비자유의사항', '사실관계',
            '당사자주장', '신청인주장', '피신청인주장', '판단', '결정사항'}


def normalize(value):
    return re.sub(r'\s+', ' ', value.replace('\u00a0', ' ')).strip()


def extract_paragraphs(body):
    """p 문단과 h4 뒤에 본문·br을 직접 두는 형식을 모두 처리한다."""
    paragraphs, buffer = [], []

    def flush():
        text = normalize(''.join(buffer))
        buffer.clear()
        if text:
            paragraphs.append(text)

    def walk(node):
        if isinstance(node, NavigableString):
            buffer.append(str(node))
            return
        if node.name in {'script', 'style'}:
            return
        boundary = node.name in {'p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'tr', 'br'}
        if boundary:
            flush()
        for child in node.children:
            walk(child)
        if boundary:
            flush()
        elif node.name in {'td', 'th'}:
            buffer.append(' ')

    if body is not None:
        walk(body)
        flush()
    return paragraphs


def parse(record, root=ROOT):
    html = BeautifulSoup((root / record['receipt']['local_path']).read_bytes(),
                         'html.parser', from_encoding='utf-8')
    body = html.select_one('.n-dbdata')
    paragraphs = extract_paragraphs(body)
    sections = {}
    current = '기타본문'
    located = []
    for index, text in enumerate(paragraphs, 1):
        key = re.sub(r'[\s▣□■○ㅇ:：\d.\-]', '', text)
        if key in HEADINGS:
            current = key
            sections.setdefault(current, [])
        else:
            sections.setdefault(current, []).append(text)
        located.append({'paragraph': index, 'section': current, 'text': text,
                        'locator': f"{record['case_id']}#p{index}"})
    text = '\n'.join(paragraphs)
    cells = record['list_cells']
    dates = [v for v in cells if re.fullmatch(r'\d{4}-\d{2}-\d{2}', v)]
    return {'case_id': record['case_id'], 'title': record['title'],
            'source_url': record['source_url'], 'publisher': record['publisher'],
            'source_type': record['source_type'], 'service': cells[2] if len(cells) > 2 else None,
            'published_date': dates[0] if dates else None, 'decision_date': None,
            'company_name': None, 'company_mapping': '원문에 명시된 회사명 검토 전: 연결 금지',
            'facts': '\n'.join(sections.get('민원내용', sections.get('사실관계', []))) or None,
            'issues': '\n'.join(sections.get('쟁점', [])) or None,
            'consumer_argument': '\n'.join(sections.get('신청인주장', [])) or None,
            'company_argument': '\n'.join(sections.get('피신청인주장', [])) or None,
            'resolution_text': '\n'.join(sections.get('처리결과', [])) or None,
            'reasoning': '\n'.join(sections.get('판단', [])) or None,
            'decision': '\n'.join(sections.get('결정사항', [])) or None,
            'caution': '\n'.join(sections.get('소비자유의사항', [])) or None,
            'sections': sections, 'paragraphs': located, 'text': text,
            'text_sha256': hashlib.sha256(normalize(text).encode()).hexdigest(),
            'retrieved_at': record['receipt']['retrieved_at'],
            'source_sha256': record['receipt']['sha256'],
            'review_status': '기계 추출: 문서별 원문 검토 필요',
            'reuse': '로컬 교육·연구 검토용; 원문 재배포 허락 미확인'}


def main():
    catalog = json.loads((ROOT / 'data/metadata/case_catalog.json').read_text('utf-8'))
    cases = [parse(r) for r in catalog]
    out = ROOT / 'data/private'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding='utf-8')
    report = {'documents': len(cases), 'unique_ids': len({c['case_id'] for c in cases}),
              'unique_bodies': len({c['text_sha256'] for c in cases}),
              'empty_bodies': [c['case_id'] for c in cases if not c['text']],
              'fields_present': {field: sum(bool(c[field]) for c in cases) for field in
                                 ['facts', 'issues', 'resolution_text', 'reasoning', 'decision', 'caution',
                                  'consumer_argument', 'company_argument', 'published_date', 'company_name']},
              'services': sorted({c['service'] or '미상' for c in cases}),
              'published_dates': sorted({c['published_date'] for c in cases if c['published_date']}),
              'important': '게시 문서 수이며 실제 민원 모집단 건수가 아니다. 한 문서에 복수 상황이 포함될 수 있다.'}
    (ROOT / 'reports/case_quality.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
