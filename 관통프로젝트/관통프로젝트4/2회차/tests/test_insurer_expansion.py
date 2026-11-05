"""실제 확보한 공식 표를 오프라인에서 다시 파싱한다. GMS/외부 HTTP 불필요."""
import hashlib
import json
import pytest
from bs4 import BeautifulSoup
from src.collection.client import ROOT,Client
from src.collection.expand_insurers import parse_knia,parse_kyobo,require_periods,main
from src.analysis.complaint_trends import insurer_total
from src.preprocessing.clean_stats import validate


def read(path):return json.loads((ROOT/path).read_text('utf-8'))


def test_all_actual_company_tables_and_periods():
    rows=read('data/processed/insurer_stats_all.json')
    report=read('reports/insurer_expansion.json')
    assert len(rows)==483 and len({r['company'] for r in rows})==18
    assert all(c['passed'] for c in validate([],rows))
    for company in {r['company'] for r in rows}:
        assert insurer_total(rows,company,'2026Q2') is not None
    for company,total in {'메리츠화재':1384,'삼성화재':2026,'현대해상':1735,
                          'KB손해보험':1502,'DB손해보험':1880,'교보생명':525}.items():
        assert insurer_total(rows,company,'2026Q2')==total
    assert report['cross_source_count']==52
    assert all(c['passed'] for c in report['checks'])


def test_raw_parser_and_original_preservation():
    sources=read('data/metadata/insurer_sources.json')
    assoc,_=parse_knia(ROOT/sources[0]['document']['local_path'],sources[0])
    life=parse_kyobo(ROOT/sources[1]['document']['local_path'],sources[1])
    assert len(assoc)==442 and len(life)==28
    base=read('data/processed/insurer_stats.json')
    combined=read('data/processed/insurer_stats_all.json')
    assert combined[:len(base)]==base and len(base)==65
    backup=ROOT/'runtime/insurers_before_20261022/data/processed/insurer_stats.json'
    if backup.exists():assert backup.read_bytes()==(ROOT/'data/processed/insurer_stats.json').read_bytes()
    for source in sources:
        p=ROOT/source['document']['local_path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==source['document']['sha256']


def test_definition_differences_and_absent_rates():
    registry=read('data/metadata/insurer_registry.json')
    assert len([c for c in registry.values() if c['sector']=='손해보험'])==17
    assert registry['교보생명']['categories']==['기타','유지','지급','판매']
    assert '즉시연금' in registry['교보생명']['caution']
    assert '이관' in registry['예별손해보험']['caution']
    rows=read('data/processed/insurer_stats_all.json')
    assert all(r['denominator_count'] is None for r in rows)
    assert all(r['rate_per_100k'] is None for r in rows if r['axis']=='상품' and r['category']=='기타')
    assert 'NH농협생명' not in registry


def test_changed_period_rejected():
    # 합성 표제만 사용하는 실패 경로 시험. 실제 기관 데이터가 아님.
    for text in ['당분기:2026년 3분기 전분기:2026년 2분기 보유계약10만건',
                 '당분기:2026년 2분기 전분기:2026년 1분기 백만건']:
        with pytest.raises(ValueError):require_periods(BeautifulSoup(text,'html.parser'))


def test_actual_cached_sources_make_no_http(monkeypatch):
    def blocked(*a,**k):raise AssertionError('오프라인 재검증에서 HTTP 금지')
    import requests
    monkeypatch.setattr(requests.sessions.Session,'request',blocked)
    client=Client()
    for s in read('data/metadata/insurer_sources.json'):client.fetch(s['source_page'],s.get('kind','html'))
    assert client.calls==0 and client.hits==3


def test_actual_manual_and_unconfirmed_product_denominators():
    from src.preprocessing.hwp_text import extract_body
    source=read('data/metadata/insurer_sources.json')[2]
    text=extract_body(ROOT/source['document']['local_path'])
    assert all(term in text for term in ['자율조정 성립','합의취하','임의철회','B2B','소송관련'])
    rows=read('data/processed/insurer_stats_all.json')
    samsung=[r for r in rows if r['company']=='삼성화재' and r['axis']=='상품']
    assert all('미확인' in r['denominator_scope'] for r in samsung)
    registry=read('data/metadata/insurer_registry.json')
    assert '미확인' in registry['삼성화재']['denominator']
    assert '미확인' not in registry['교보생명']['denominator']
