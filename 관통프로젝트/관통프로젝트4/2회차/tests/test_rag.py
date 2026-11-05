"""Contract and graph tests use visibly synthetic doubles, not semantic vectors."""
import pytest
from src.rag.pipeline import validate_answer, validate_keywords, validate_selection, Pipeline, QueryCache
from src.rag.config import settings, fingerprint


def test_output_contract_rejects_nonexistent_or_mismatched_citation():
    with pytest.raises(ValueError):
        validate_answer({'answer': '테스트 주장 [9]', 'status': '근거 있음', 'cited_numbers': [9]}, [{}])
    with pytest.raises(ValueError):
        validate_answer({'answer': '테스트 주장 [1]', 'status': '근거 있음', 'cited_numbers': []}, [{}])
    assert validate_answer({'answer': '인용 없는 합성 답변', 'status': '근거 있음', 'cited_numbers': []}, [{}])['status'] == '확인 불가'


def test_candidates_and_keywords_have_strict_types():
    with pytest.raises(ValueError):
        validate_selection({'selected_ids': ['not_allowed']}, {'case_a'})
    with pytest.raises(ValueError):
        validate_keywords({'in_scope': 'true', 'keywords': ['보험']})
    with pytest.raises(ValueError):
        validate_keywords({'in_scope': True, 'keywords': [12]})
    assert validate_selection({'selected_ids': ['case_a', 'case_a']}, {'case_a'}) == ['case_a']


def test_collection_configuration_isolation():
    cfg = settings()
    for field, value in [('chunk_size', 400), ('chunk_overlap', 30), ('mode', 'other_mode')]:
        assert fingerprint(cfg) != fingerprint(cfg | {field: value})
    assert fingerprint(cfg) == fingerprint(cfg | {'top_k': 3})


def test_two_node_graph_out_of_scope_never_collects(tmp_path):
    class ForbiddenCollector:
        def own_document(self, item):
            raise AssertionError('Out-of-scope questions must not collect documents')
    class SyntheticStore:
        pass
    pipeline = Pipeline(settings(), SyntheticStore(), [], collector=ForbiddenCollector(), cache=QueryCache(tmp_path / 'cache.db'))
    state = pipeline.run({'item_id': 'synthetic_item'}, '해외주식 양도소득세 신고방법')
    assert state['result']['status'] == '확인 불가'
    assert state['sources'] == []
    assert set(pipeline.graph.get_graph().nodes) == {'__start__', 'retrieve', 'generate', '__end__'}


def test_company_filters_survive_case_navigation_and_back():
    from streamlit.testing.v1 import AppTest
    from src.collection.client import ROOT
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=30).run()
    next(s for s in app.selectbox if s.key == '_company_ui').set_value('삼성화재').run()
    next(s for s in app.selectbox if s.key == '_company_period_ui').set_value('2026Q1').run()
    next(w for w in app.button_group if w.key == 'workspace').set_value('사례 탐색').run()
    next(w for w in app.button_group if w.key == 'workspace').set_value('업무 개요').run()
    assert not app.exception
    assert next(s for s in app.selectbox if s.key == '_company_ui').value == '삼성화재'
    assert next(s for s in app.selectbox if s.key == '_company_period_ui').value == '2026Q1'
    assert app.metric[0].value == '2,199건'


def test_rag_page_does_not_call_gms_on_open():
    from streamlit.testing.v1 import AppTest
    from src.collection.client import ROOT
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=30).run()
    next(w for w in app.button_group if w.key == 'workspace').set_value('근거 기반 AI').run()
    assert not app.exception
    assert any(b.key == 'rag_prepare' for b in app.button)
    assert any('범위:' in c.value for c in app.caption)


def test_missing_period_rejects_wrong_model_answer(tmp_path):
    class SyntheticStore:
        def retrieve(self, *args):
            return [{'title': '합성 시험 항목', 'text': '선택기간 2026Q2', 'item_id': 'synthetic'}]
    class SyntheticModel:
        def json(self, *args):
            return {'answer': '합성 잘못된 현재 수치 답변 [1]', 'status': '근거 있음', 'cited_numbers': [1]}
    pipeline = Pipeline(settings(), SyntheticStore(), [], gms=SyntheticModel(), collector=object(), cache=QueryCache(tmp_path / 'cache.db'))
    state = pipeline.run({'item_id': 'synthetic', 'text': '2026Q2', 'company': '합성 시험 회사', 'period': '2026Q2'}, '2030년 2분기 민원은 몇 건이야?')
    assert state['result']['status'] == '확인 불가'
    assert state['result']['model_answer_rejected'] is True
