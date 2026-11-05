"""테스트의 작은 가짜 HTML/HTTP 객체는 실제 사례/수집 결과와 명확히 분리한다."""
import json
from datetime import datetime, timezone
from pathlib import Path
import pytest
from bs4 import BeautifulSoup
from src.collection.client import Client, ROOT, retry_delay
from src.preprocessing.parse_cases import extract_paragraphs
from src.preprocessing.clean_stats import number, validate
from src.analysis.case_search import CaseSearch, validate_citation
from src.analysis.complaint_trends import growth, comparable_periods, insurer_total, validate_company_case_link


@pytest.fixture(scope='module')
def cases():
    return json.loads((ROOT/'data/private/cases.json').read_text('utf-8'))


@pytest.fixture(scope='module')
def statistics():
    return [json.loads((ROOT/f'data/processed/{n}.json').read_text('utf-8'))
            for n in ['sector_stats','insurer_stats']]


def test_inline_body_and_spans():
    html=BeautifulSoup('<div><h4>▣ 민원내용</h4>실제<span>본문</span><br>다음 문장<p>문단<span>내용</span></p></div>', 'html.parser')
    assert extract_paragraphs(html.div)==['▣ 민원내용','실제본문','다음 문장','문단내용']


def test_actual_documents(cases):
    assert len(cases)>=30
    assert len({c['case_id'] for c in cases})==len(cases)
    assert len({c['text_sha256'] for c in cases})==len(cases)
    assert all(c['facts'] and c['issues'] and c['resolution_text'] for c in cases)
    assert all(len(c['text'])>200 for c in cases)


def test_unknown_fields_not_invented(cases):
    assert all(c['decision_date'] is None and c['company_name'] is None for c in cases)
    assert all(c['consumer_argument'] is None and c['company_argument'] is None for c in cases)
    assert not any(validate_company_case_link(c,'하나손해보험') for c in cases)


def test_all_paragraphs_addressable(cases):
    for c in cases:
        for p in c['paragraphs']:
            assert validate_citation(cases,c['case_id'],p['paragraph'],p['text'])
        assert not validate_citation(cases,c['case_id'],999,'없는 문단')


def test_false_and_cross_document_citations(cases):
    c=cases[0];p=next(p for p in c['paragraphs'] if len(p['text'])>35)
    assert not validate_citation(cases,'없는 문서',p['paragraph'],p['text'])
    assert not validate_citation(cases,cases[1]['case_id'],p['paragraph'],p['text'])
    assert not validate_citation(cases,c['case_id'],p['paragraph'],'이 사례는 무조건 보상된다')
    assert not validate_citation(cases,c['case_id'],p['paragraph'],'')


def test_search_returns_actual_excerpt(cases):
    search=CaseSearch(cases)
    hits=search.search('백내장 다초점 인공수정체 수술')
    assert any(h['case_id'] in {'fss_case_71','fss_case_162'} for h in hits)
    assert all(validate_citation(cases,h['case_id'],p['paragraph'],p['text']) for h in hits for p in h['excerpts'])
    assert search.search('')==[]
    assert search.search('zzzzzzzzzz')==[]
    assert search.search('자동차',service='없는분야')==[]
    with pytest.raises(ValueError):search.search('질문',0)


def test_actual_statistics_and_sums(statistics):
    sectors,insurers=statistics
    assert all(c['passed'] for c in validate(sectors,insurers))
    assert insurer_total(insurers,'하나손해보험','2026Q2')==75
    assert insurer_total(insurers,'신한EZ손해보험','2026Q2')==89
    assert insurer_total(insurers,'없는회사','2026Q2') is None


def test_period_and_growth_guard():
    assert not comparable_periods({'period':'2025','period_type':'연간'},{'period':'2026H1','period_type':'반기'})
    assert comparable_periods({'period':'2025H1','period_type':'반기'},{'period':'2026H1','period_type':'반기'})
    assert growth(0,5) is None
    assert growth(50,75)==50
    with pytest.raises(ValueError):growth(-1,3)


def test_missing_rate_is_not_zero():
    assert number('-') is None
    assert number('0.00')==0
    assert number('△12.5')==-12.5


def test_retry_after():
    now=datetime(2026,10,22,0,0,0,tzinfo=timezone.utc)
    assert retry_delay('7',0,now)==7
    assert retry_delay('Thu, 22 Oct 2026 00:00:09 GMT',0,now)==9
    assert retry_delay('unknown',2,now)==4
    with pytest.raises(RuntimeError):retry_delay('120',0,now)


class Response:
    # 오프라인 네트워크 시험용 객체: 실제 기관 응답이 아님.
    def __init__(self,status=200,content=b'demo',headers=None):
        self.status_code=status;self.content=content;self.headers=headers or {};self.url='https://www.fss.or.kr/test'
        self.text=content.decode('utf-8')
    def raise_for_status(self):
        if self.status_code>=400:raise RuntimeError('HTTP 테스트 오류')


def test_retry_and_external_redirect(monkeypatch,tmp_path):
    import src.collection.client as mod
    monkeypatch.setattr(mod,'sleep',lambda seconds:None)
    c=Client(tmp_path);responses=iter([Response(429,headers={'Retry-After':'0'}),Response(503),Response()])
    monkeypatch.setattr(c.session,'get',lambda *a,**k:next(responses))
    assert c._request('https://www.fss.or.kr/test').content==b'demo'
    assert c.calls==3
    monkeypatch.setattr(c.session,'get',lambda *a,**k:Response(302,headers={'Location':'https://other.example/'}))
    with pytest.raises(ValueError):c._request('https://www.fss.or.kr/test')


def test_persistent_cache_integrity_and_robots(monkeypatch,tmp_path):
    c=Client(tmp_path)
    from urllib.robotparser import RobotFileParser
    rp=RobotFileParser();rp.parse(['User-agent: *','Allow: /'])
    monkeypatch.setattr(c,'policy',lambda host:rp)
    calls=[]
    monkeypatch.setattr(c,'_request',lambda url:(calls.append(url) or Response(content=b'private-cache-test')))
    first,record=c.fetch('https://www.fss.or.kr/test')
    second,_=c.fetch('https://www.fss.or.kr/test')
    assert first==second and len(calls)==1 and c.hits==1
    first.write_text('tampered',encoding='utf-8')
    with pytest.raises(ValueError):c.fetch('https://www.fss.or.kr/test')
    rp=RobotFileParser();rp.parse(['User-agent: *','Disallow: /'])
    with pytest.raises(PermissionError):c.fetch('https://www.fss.or.kr/blocked')
    with pytest.raises(ValueError):c.fetch('https://www.kca.go.kr/blocked')


def test_pdf_html_crosscheck_passed():
    checks=json.loads((ROOT/'reports/cross_source_validation.json').read_text('utf-8'))
    assert len(checks)==13 and all(c['passed'] for c in checks)
