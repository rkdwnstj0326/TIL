"""실제 로컬 데이터로 사용자 흐름을 검사한다. 외부 HTTP와 GMS는 차단한다."""
import pytest
from streamlit.testing.v1 import AppTest
from src.collection.client import ROOT


@pytest.fixture
def app(monkeypatch):
    import requests
    def blocked(*args,**kwargs):
        raise AssertionError('자동 화면 검사 중 외부 HTTP 요청 금지')
    monkeypatch.setattr(requests.sessions.Session,'request',blocked)
    app=AppTest.from_file(str(ROOT/'app.py'),default_timeout=30).run()
    assert not app.exception
    return app


def go(app,name):
    next(w for w in app.button_group if w.key=='workspace').set_value(name).run()
    assert not app.exception


def test_business_overview(app):
    assert [m.value for m in app.metric]==['75건','+7건','55건','6.02']
    assert len([b for b in app.button if b.key and b.key.startswith('review_')])==3


def test_company_and_period_filters_persist(app):
    next(s for s in app.selectbox if s.key=='_company_period_ui').set_value('2026Q1').run()
    assert not app.exception
    assert app.metric[0].value=='68건'
    next(s for s in app.selectbox if s.key=='_company_ui').set_value('신한EZ손해보험').run()
    assert not app.exception
    assert app.metric[0].value=='54건'
    go(app,'민원 분석')
    assert app.metric[0].value=='54건'
    next(s for s in app.selectbox if s.key=='_company_period_ui').set_value('2026Q2').run()
    assert app.metric[0].value=='89건'
    go(app,'업무 개요')
    assert [m.value for m in app.metric][:3]==['89건','+35건','87건']
    assert len([b for b in app.button if b.key and b.key.startswith('review_')])==2


def test_sector_analysis_and_missing_product_rate(app):
    go(app,'민원 분석')
    next(r for r in app.radio if r.label=='민원 분류').set_value('상품').run()
    next(s for s in app.selectbox if s.label=='표시 지표').set_value('보유계약 10만건당').run()
    assert not app.exception
    next(r for r in app.radio if r.key=='analysis_level').set_value('금감원 동향').run()
    assert not app.exception
    assert [m.value for m in app.metric][:2]==['28,137건','39,963건']
    next(s for s in app.selectbox if s.label=='비교 기간').set_value('연간끼리 비교').run()
    assert not app.exception
    assert [m.value for m in app.metric][:2]==['53,450건','62,937건']


def test_review_card_opens_real_related_evidence(app):
    next(b for b in app.button if b.key=='review_1').click().run()
    assert not app.exception
    assert app.session_state['workspace']=='사례 탐색'
    hits=app.session_state['finvoc_hits']
    assert any(h['case_id']=='fss_case_73' for h in hits)
    assert app.session_state['last_query']=='보험금 청구 진료비 영수증 추가 서류'
    assert '하나손해보험' not in app.session_state['last_query']


def test_search_example_selection_and_no_results(app):
    go(app,'사례 탐색')
    next(b for b in app.button if b.key=='example_백내장 수술').click().run()
    assert not app.exception
    hits=app.session_state['finvoc_hits']
    assert 'fss_case_162' in [h['case_id'] for h in hits]
    assert 'fss_case_71' not in [h['case_id'] for h in hits]
    assert app.session_state['search_group']=='실손보험'
    if len(hits)>1:
        second=hits[1]['case_id']
        next(b for b in app.button if b.key=='open_'+second).click().run()
        assert not app.exception
        assert app.session_state['selected_case']==second
    next(i for i in app.text_input if i.key=='search_query').set_value('zzzzzzzzzz')
    next(b for b in app.button if b.label=='관련 사례 검색').click().run()
    assert not app.exception
    assert app.session_state['finvoc_hits']==[]
    assert any('찾지 못했습니다' in w.value for w in app.warning)


def test_data_management_is_separate(app):
    go(app,'자료 관리')
    assert [m.value for m in app.metric]==['2,331개 관측값','70개','85개','957/957'] or [m.value for m in app.metric]==['2331개 관측값','70개','85개','957/957']
    assert any('자동 수집' in c.value for c in app.caption)
    assert any('독립 성능평가 아님' in str(df.value) for df in app.dataframe)


def test_expanded_companies_and_life_definitions(app):
    company=next(s for s in app.selectbox if s.key=='_company_ui')
    assert len(company.options)==19
    assert 'MG손해보험' in company.options and '캐롯손해보험' in company.options
    company.set_value('삼성화재').run()
    assert not app.exception
    assert [m.value for m in app.metric]==['2,026건','-173건','1,597건','5.81']
    go(app,'민원 분석')
    next(r for r in app.radio if r.label=='민원 분류').set_value('상품').run()
    next(s for s in app.selectbox if s.label=='표시 지표').set_value('보유계약 10만건당').run()
    assert not app.exception
    assert any('비교 차트는 표시하지 않습니다' in i.value for i in app.info)
    next(s for s in app.selectbox if s.key=='_insurer_sector_ui').set_value('생명보험').run()
    assert not app.exception
    assert next(s for s in app.selectbox if s.key=='_company_ui').value=='교보생명'
    assert [m.value for m in app.metric]==['525건','-36건','385건','5.47']
    assert app.metric[2].label=='지급 유형'
    assert any('즉시연금' in c.value for c in app.caption)
    go(app,'민원 분석')
    assert not app.exception
    next(r for r in app.radio if r.label=='민원 분류').set_value('상품').run()
    next(s for s in app.selectbox if s.label=='표시 지표').set_value('보유계약 10만건당').run()
    assert not app.exception


def test_source_text_cannot_execute_html():
    # 합성 시험 문자열이며 실제 금감원 자료가 아니다.
    app=AppTest.from_string("from src.ui.components import source_text\nsource_text('<script>secret()</script>\\n원문 & 조건')").run()
    assert not app.exception
    content=next(m.value for m in app.markdown if 'sourcebox' in m.value)
    assert '&lt;script&gt;' in content and '<script>' not in content
    assert '&amp;' in content
