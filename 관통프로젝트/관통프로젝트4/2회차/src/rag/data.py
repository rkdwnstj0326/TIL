"""Company-quarter items stay separate from anonymous industry case documents."""
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from src.collection.client import ROOT, Client
from src.analysis.dashboard import snapshot
from src.analysis.case_search import CaseSearch
from src.preprocessing.parse_cases import parse


def read(relative):
    return json.loads((ROOT / relative).read_text('utf-8'))


def corpus():
    history=ROOT/'data/processed/insurer_stats_history.json'
    return read('data/processed/insurer_stats_history.json' if history.exists() else 'data/processed/insurer_stats_all.json'), read('data/private/cases.json')


def items(rows=None):
    rows = corpus()[0] if rows is None else rows
    registry = read('data/metadata/insurer_registry_history.json' if (ROOT/'data/metadata/insurer_registry_history.json').exists() else 'data/metadata/insurer_registry.json')
    result = []
    for company, period in sorted({(r['company'], r['period']) for r in rows}):
        selected = [r for r in rows if r['company'] == company and r['period'] == period]
        details = dict(registry.get(company, {}))
        if any(r['axis']=='상품' and '미확인' in r.get('denominator_scope','') for r in selected):
            details['denominator']='회사 전체 환산단위는 10만건당. 해당기간 상품 상세 분모(상품별/전체)는 협회 표에서 미확인.'
        data = snapshot(rows, company, period)
        prior_display=f'{data["previous_total"]}건' if data['previous_total'] is not None else '자료 없음'
        change_display='공시기준 변경으로 비교 보류(0건 변화가 아님)' if data['comparison_blocked'] else f'{data["change"]}건' if data['change'] is not None else '비교 자료 없음'
        item_id = 'insurer_' + hashlib.sha256(company.encode()).hexdigest()[:12] + '_' + period
        text = '\n'.join([
            f'보험사: {company}; 공시기간: {period}; 업권: {details.get("sector", "미확인")}',
            f'민원 합계(접수경로 기준): {data["total"]}건; 직전 분기({data["previous_period"]}) 합계: {prior_display}',
            f'직전 분기 대비 증감: {change_display}',
            f'분모: {details.get("denominator", "미확인")}',
            f'비교 주의: {details.get("caution", "회사간 단순 순위 금지")}',
            f'이 기간 공시기준: {data["definition_regime"]}; 전분기 기준 변경으로 증감 비교 보류: {data["comparison_blocked"]}',
            '단위 구분: 민원건수는 실제 접수 건수(건). 보유계약10만건당 환산건수는 별도 지표이며 민원건수 자체가 환산값인 것은 아닙니다. 비교 보류는 증감0건이 아닙니다.',
            '분류축별 행은 동일 민원의 다른 구분입니다. 분류축을 합산하지 마세요.',
            *[f'{r["axis"]}/{r["category"]}: {r["count"]}건; 보유계약10만건당={r["rate_per_100k"]}; 단위={r.get("rate_unit", "미확인")}' for r in selected],
            '익명 업계 사례는 이 보험사의 사건으로 확인되지 않았습니다.'
        ])
        urls = sorted({r['source_url'] for r in selected})
        dates = []
        for url in urls:
            receipt = ROOT / 'data/metadata' / (hashlib.sha256(url.encode()).hexdigest() + '.json')
            if receipt.exists():
                dates.append(json.loads(receipt.read_text('utf-8'))['retrieved_at'])
        result.append({'item_id': item_id, 'company': company, 'period': period,
            'title': company + ' · ' + period, 'text': text, 'rows': selected,
            'url': urls[0], 'source_type': '회사·분기 공시 메타데이터',
            'collected_at': min(dates) if dates else '미확인', 'sector': details.get('sector', '미확인'),
            'total': data['total'], 'denominator': details.get('denominator', '미확인')})
        result[-1]['comparison_blocked']=data['comparison_blocked']
        result[-1]['available_periods']=[period]+([data['previous_period']] if data['previous_total'] is not None else [])
    return result


def candidates(question, keywords, cases, limit=8):
    search = CaseSearch(cases)
    merged = {}
    for query in [question, *keywords]:
        for rank, hit in enumerate(search.search(query, k=min(limit, 20))):
            if hit['score'] < 0.035:
                continue
            cid = hit['case_id']
            if cid not in merged:
                merged[cid] = hit | {'rank_score': 0.0}
            merged[cid]['rank_score'] += 1 / (20 + rank)
    return sorted(merged.values(), key=lambda h: -h['rank_score'])[:limit]


class DocumentCollector:
    def __init__(self):
        self.client = Client()

    def own_document(self, item):
        """Fetch/validate the actual source at question time, then use located table rows."""
        receipts = []
        for url in sorted({r['source_url'] for r in item['rows']}):
            kind = 'pdf' if any(r.get('source_page') for r in item['rows'] if r['source_url'] == url) else 'html'
            _, receipt = self.client.fetch(url, kind)
            receipts.append(receipt)
        # These are extracted original table rows, not fabricated model summaries.
        body = '\n'.join([f'{item["company"]} {item["period"]} 공시 원문에서 추출한 행. 선택 기간의 정제값과 함께 읽으세요.',
            *[f'선택기간 {r["period"]} / {r["axis"]} / {r["category"]}: {r["count"]}건; 원문 행: {r["source_row"]}; 페이지: {r.get("source_page") or "HTML 표"}' for r in item['rows']],
            '원문 행에 전분기와 당분기 열이 함께 있는 경우 선택기간의 정제값을 기준으로 합니다.'])
        return {'doc_id': 'self_' + item['item_id'], 'title': item['title'] + ' 공시 원문 행',
            'url': item['url'], 'source_type': '선택 보험사·분기 자체 공시',
            'collected_at': min(r['retrieved_at'] for r in receipts), 'text': body,
            'paragraphs': [{'paragraph': i + 1, 'text': line} for i, line in enumerate(body.splitlines())],
            'event_company_name': item['company'], 'is_self': True}

    def case_document(self, case_id):
        catalog = read('data/metadata/case_catalog.json')
        record = next((r for r in catalog if r['case_id'] == case_id), None)
        if record is None:
            raise ValueError('허용된 공식 목록에 없는 문서입니다.')
        _, receipt = self.client.fetch(record['source_url'])
        parsed = parse(record | {'receipt': receipt})
        paragraphs = [p for p in parsed['paragraphs'] if len(p['text'].strip()) >= 35]
        if not paragraphs:
            raise ValueError('제목을 제외한 본문이 없습니다.')
        return {'doc_id': parsed['case_id'], 'title': parsed['title'], 'url': parsed['source_url'],
            'source_type': '금감원 공개 업계 사례(회사 미확인)', 'collected_at': parsed['retrieved_at'],
            'text': '\n'.join(p['text'] for p in paragraphs), 'paragraphs': paragraphs,
            'event_company_name': '', 'is_self': False}
