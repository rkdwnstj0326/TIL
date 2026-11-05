"""Real historical source parsing, exclusions, regime boundary and UI integration."""
import hashlib,json
import pytest
from streamlit.testing.v1 import AppTest
from src.collection.client import ROOT,Client
from src.collection.expand_insurers import parse_knia
from src.analysis.dashboard import snapshot
from src.preprocessing.clean_stats import validate
from src.rag.data import corpus,items


def read(relative):return json.loads((ROOT/relative).read_text('utf-8'))


def test_history_preserves_baseline_and_has_real_quarters():
    baseline=read('data/processed/insurer_stats_all.json')
    rows=read('data/processed/insurer_stats_history.json')
    report=read('reports/insurer_history.json')
    assert rows[:len(baseline)]==baseline and len(baseline)==483
    assert len(rows)==2303
    assert len({(r['company'],r['period']) for r in rows})==177
    assert {r['period'] for r in rows}=={f'{year}Q{q}' for year in [2024,2025] for q in [1,2,3,4]}|{'2026Q1','2026Q2'}
    assert all(c['passed'] for c in validate([],rows))
    assert report['baseline_sha256']==hashlib.sha256((ROOT/'data/processed/insurer_stats_all.json').read_bytes()).hexdigest()
    assert all(c['passed'] for c in report['overlap_cross_checks'])


def test_real_historical_html_period_not_just_request_parameter():
    source=read('data/metadata/insurer_history_sources.json')[0]
    rows,_=parse_knia(ROOT/source['document']['local_path'],source,['2024Q1','2024Q2'])
    assert {r['period'] for r in rows}=={'2024Q1','2024Q2'}
    with pytest.raises(ValueError):
        parse_knia(ROOT/source['document']['local_path'],source,['2025Q1','2025Q2'])


def test_inconsistent_aig_records_stay_excluded_and_periods_not_filled():
    rows=read('data/processed/insurer_stats_history.json')
    report=read('reports/insurer_history.json')
    for period in ['2024Q3','2024Q4','2025Q1']:
        assert not any(r['company']=='AIG손해보험' and r['period']==period for r in rows)
        assert any(e['company']=='AIG손해보험' and e['period']==period for e in report['excluded'])
    assert not any(r['company']=='교보생명' and r['period'].startswith('2025') for r in rows)


def test_definition_change_blocks_growth_and_company_transfer_is_separate():
    rows=read('data/processed/insurer_stats_history.json')
    at_boundary=snapshot(rows,'하나손해보험','2024Q2')
    assert at_boundary['previous_total'] is not None
    assert at_boundary['comparison_blocked'] is True
    assert at_boundary['change'] is None and at_boundary['growth'] is None
    assert not snapshot(rows,'하나손해보험','2025Q2')['comparison_blocked']
    assert {'MG손해보험','예별손해보험','캐롯손해보험','한화손해보험'} <= {r['company'] for r in rows}


def test_rag_and_app_select_past_quarter_without_live_gms():
    assert len(items())==177 and len(corpus()[0])==2303
    old=next(i for i in items() if i['company']=='하나손해보험' and i['period']=='2024Q2')
    assert '전분기 기준 변경으로 증감 비교 보류: True' in old['text']
    assert '미확인' in old['denominator']
    app=AppTest.from_file(str(ROOT/'app.py'),default_timeout=30).run()
    period=next(s for s in app.selectbox if s.key=='_company_period_ui')
    assert len(period.options)==10
    period.set_value('2024Q2').run()
    assert not app.exception
    assert app.metric[1].value=='비교 보류'
    assert any('공시기준 개선' in w.value for w in app.warning)


def test_historical_source_cache_no_http(monkeypatch):
    import requests
    def blocked(*args,**kwargs):raise AssertionError('No HTTP in historical cache regression test')
    monkeypatch.setattr(requests.sessions.Session,'request',blocked)
    client=Client()
    for s in read('data/metadata/insurer_history_sources.json'):client.fetch(s['source_page'])
    assert client.calls==0 and client.hits==4
