"""공식 표에서 관측값을 추출하고 출처의 기간·단위·분류축을 함께 저장한다."""
import json
import re
from bs4 import BeautifulSoup
from src.collection.client import ROOT


def number(value):
    value = value.strip().replace(',', '').replace('△', '-')
    if value in {'', '-'}:
        return None
    return float(value) if '.' in value else int(value)


def load_sources():
    return {s['source_id']: s for s in json.loads(
        (ROOT / 'data/metadata/source_catalog.json').read_text('utf-8'))}


def pdf_text(source_id, page):
    pages = json.loads((ROOT / f'data/private/extracted/{source_id}.json').read_text('utf-8'))
    return next(p['text'] for p in pages if p['page'] == page)


def sector_stats(sources):
    rows = []
    # 각 줄에 2024 연간, 2025 연간, 2025 상반기, 2026 상반기가 차례로 있다.
    text = pdf_text('kdi_287509', 9)
    labels = {'금융민원': '금융민원', '은행': '은행', '중소서민': '중소서민',
              '보험': '보험', '생명보험': '생명보험', '손해보험': '손해보험', '금융투자': '금융투자'}
    for line in text.splitlines():
        compact = re.sub(r'\s+', '', line)
        for label in labels:
            if not compact.startswith(label) or '(' in compact:
                continue
            tail = compact[len(label):]
            # 라벨 뒤에 다른 글자가 있으면 보험/생명보험 등의 부분일치로 취급하지 않는다.
            if not tail or not tail[0].isdigit():
                continue
            values = re.findall(r'\d[\d,]*(?:\.\d+)?', line)
            if len(values) != 6:
                raise ValueError(f'권역 표의 열 개수 변경: {label}')
            for period, value in zip(['2024', '2025', '2025H1', '2026H1'], values[:4]):
                rows.append({'sector': label, 'period': period, 'period_type': '반기' if 'H' in period else '연간',
                             'count': int(number(value)), 'unit': '건', 'metric': '금융민원 접수',
                             'source_id': 'kdi_287509', 'source_url': sources['kdi_287509']['source_page'],
                             'source_page': 9, 'source_row': line.strip(),
                             'definition': '접수일 기준; 중복·반복 및 단순 질의·건의 등 제외; 추후 재분류 가능'})
    if len(rows) != 28:
        raise ValueError(f'권역 표 예상 28개 관측값, 실제 {len(rows)}')
    return rows


def observations(company, axis, label, values, periods, source, page, evidence):
    if len(values) != 6:
        raise ValueError('민원건수·환산건수 표의 6개 숫자 열이 필요합니다.')
    records = []
    for i, period in enumerate(periods):
        records.append({'company': company, 'period': period, 'period_type': '분기', 'axis': axis,
                        'category': re.sub(r'\s+', '', label), 'count': number(values[i]),
                        'rate_per_100k': number(values[i + 3]),
                        'rate_unit': '해당 분기말 보유계약 10만건당',
                        'denominator_scope': '상품별 보유계약' if axis == '상품' else '회사 전체 보유계약',
                        'denominator_count': None, 'source_id': source['source_id'],
                        'source_url': source['source_page'], 'source_page': page,
                        'source_row': evidence, 'reported_count_change_pct': number(values[2]),
                        'reported_rate_change_pct': number(values[5]),
                        'definition': '공시 원문 기준; 자체·대외/유형/상품은 같은 민원의 다른 분류축. 축간 합산 금지'})
    return records


def insurer_stats(sources):
    records = []
    hana = sources['hana_2026q1']
    text26, text27 = pdf_text('hana_2026q1', 26), pdf_text('hana_2026q1', 27)
    spans = [('접수경로', text26.split('7-3-1)')[1].split('7-3-2)')[0],
              ['자체민원', '대외민원', '합계']),
             ('유형', text26.split('7-3-2)')[1], ['보험모집', '유지관리', '보상(보험금)', '기타', '합계']),
             ('상품', text27.split('주1) 해당')[0],
              ['일반보험', '장기보장성보험', '장기저축성보험', '자동차보험', '기타'])]
    for axis, text, labels in spans:
        found = []
        for line in text.splitlines():
            # PDF 문단의 행별 추출값을 사용한다. 표 검출기는 소수점을 별도 줄에 놓을 수 있다.
            label = next((label for label in labels if re.sub(r'\s+', '', label) in
                          re.sub(r'\s+', '', line)), None)
            if label is None:
                continue
            # 각 행의 라벨 뒤 숫자만. '기타주1)'의 주석 번호는 제거한다.
            clean = re.sub(r'주\d+\)', '', line)
            vals = re.findall(r'-?\d+(?:\.\d+)?|(?<=\s)-(?=\s|$)', clean)
            if len(vals) != 6:
                continue
            found.append(label)
            records.extend(observations('하나손해보험', axis, label, vals,
                                        ['2025Q4', '2026Q1'], hana, 27 if axis == '상품' else 26, line.strip()))
        if set(found) != set(labels):
            raise ValueError(f'하나 {axis} 누락/양식변경: {set(labels)-set(found)}')
    shinhan = sources['shinhanez_2026q2']
    html = BeautifulSoup((ROOT / shinhan['document']['local_path']).read_bytes(),
                         'html.parser', from_encoding='utf-8')
    if '2026.01.01 ~ 2026.03.31' not in html.get_text(' ', strip=True):
        raise ValueError('신한EZ 비교 기간 원문 확인 필요')
    for axis, table in zip(['접수경로', '유형', '상품'], html.select('table'), strict=True):
        for tr in table.select('tr'):
            cells = [c.get_text(' ', strip=True) for c in tr.find_all(['th', 'td'], recursive=False)]
            if cells and cells[0] in {'유형', '상품'}:
                cells = cells[1:]
            if len(cells) != 8 or cells[0] in {'구분', '전분기'}:
                continue
            try:
                records.extend(observations('신한EZ손해보험', axis, cells[0], cells[1:7],
                                            ['2026Q1', '2026Q2'], shinhan, None, ' | '.join(cells)))
            except ValueError:
                if any(v.isdigit() for v in cells[1:3]):
                    raise
    # 하나의 최신 HTML은 여러 분기를 숨겨 둔다. 해당 DOM 구역만 선택해 섞이지 않게 한다.
    disclosure = sources['hana_disclosures']
    hana_html = BeautifulSoup((ROOT / disclosure['document']['local_path']).read_bytes(),
                             'html.parser', from_encoding='utf-8').select_one('#table_2026_2')
    if hana_html is None:
        raise ValueError('하나 2026년 2분기 공식 공시 구역 누락')
    overlap_checks = []
    for axis, table in zip(['접수경로', '유형', '상품'], hana_html.select('table'), strict=True):
        for tr in table.select('tbody tr, tfoot tr'):
            cells = []
            for td in tr.find_all(['th', 'td'], recursive=False):
                # 각주 번호는 숫자 관측값/분류명에 포함하지 않는다.
                for sup in td.select('sup'):
                    sup.decompose()
                cells.append(td.get_text(' ', strip=True))
            if cells and cells[0] in {'유형', '상품'}:
                cells = cells[1:]
            if len(cells) != 8:
                raise ValueError('하나 HTML 표 열 개수 변경')
            pair = observations('하나손해보험', axis, cells[0], cells[1:7],
                                ['2026Q1', '2026Q2'], disclosure, None, ' | '.join(cells))
            previous = next(r for r in records if r['company'] == '하나손해보험' and
                            r['period'] == '2026Q1' and r['axis'] == axis and r['category'] == pair[0]['category'])
            matched = previous['count'] == pair[0]['count'] and previous['rate_per_100k'] == pair[0]['rate_per_100k']
            overlap_checks.append({'check': f"하나 PDF↔HTML 2026Q1 {axis} {pair[0]['category']}", 'passed': matched})
            records.append(pair[1])
    (ROOT / 'reports/cross_source_validation.json').write_text(
        json.dumps(overlap_checks, ensure_ascii=False, indent=2), encoding='utf-8')
    if not all(c['passed'] for c in overlap_checks):
        raise ValueError('하나 1분기 PDF와 2분기 HTML의 전분기 수치가 일치하지 않습니다.')
    return records


def validate(sectors, insurers):
    checks = []
    for period in sorted({r['period'] for r in sectors}):
        values = {r['sector']: r['count'] for r in sectors if r['period'] == period}
        checks.append({'check': f'{period} 보험=생명+손해',
                       'passed': values['보험'] == values['생명보험'] + values['손해보험']})
        checks.append({'check': f'{period} 전체=은행+중소서민+보험+투자',
                       'passed': values['금융민원'] == sum(values[k] for k in ['은행','중소서민','보험','금융투자'])})
    for company, period in sorted({(r['company'], r['period']) for r in insurers}):
        group = [r for r in insurers if r['company'] == company and r['period'] == period]
        totals = {}
        for axis in ['접수경로', '유형', '상품']:
            rows = [r for r in group if r['axis'] == axis]
            parts = sum(r['count'] for r in rows if r['category'] != '합계')
            total = next((r['count'] for r in rows if r['category'] == '합계'), parts)
            checks.append({'check': f'{company} {period} {axis} 부분합', 'passed': total == parts})
            totals[axis] = total
        checks.append({'check': f'{company} {period} 세 분류축의 총수 일치',
                       'passed': len(set(totals.values())) == 1})
    keys = [(r['company'], r['period'], r['axis'], r['category']) for r in insurers]
    checks.append({'check': '회사 통계 관측키 유일', 'passed': len(keys) == len(set(keys))})
    checks.append({'check': '민원건수 음수/결측 없음',
                   'passed': all(isinstance(r['count'], int) and r['count'] >= 0 for r in insurers)})
    return checks


def main():
    sources = load_sources()
    sectors, insurers = sector_stats(sources), insurer_stats(sources)
    checks = validate(sectors, insurers)
    if not all(c['passed'] for c in checks):
        raise ValueError(json.dumps(checks, ensure_ascii=False))
    target = ROOT / 'data/processed'
    target.mkdir(parents=True, exist_ok=True)
    for name, rows in [('sector_stats', sectors), ('insurer_stats', insurers)]:
        (target / (name + '.json')).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    report = {'sector_observations': len(sectors), 'insurer_observations': len(insurers),
              'checks': checks, 'warning': '회사 분기 공시와 금감원 접수 통계는 접수범위·분모기준이 다르므로 혼합 금지'}
    (ROOT / 'reports/statistics_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'sector_observations': len(sectors), 'insurer_observations': len(insurers),
                      'checks_passed': sum(c['passed'] for c in checks)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
