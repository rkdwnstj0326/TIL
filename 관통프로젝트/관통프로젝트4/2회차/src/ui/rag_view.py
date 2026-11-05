"""Grounded answers, item-isolated conversations and explicit indexing controls."""
import json
import re
import time
import streamlit as st
from src.collection.client import ROOT
from src.rag.config import settings, fingerprint, key_configured
from src.rag.data import items
from src.rag.gms import GMS, GMSError
from .components import page_intro, source_text, source_button


@st.cache_resource(show_spinner=False)
def resources(signature):
    from src.rag.embedding import LocalEmbedding
    from src.rag.store import Store
    cfg = settings()
    embed = LocalEmbedding(cfg)
    return Store(cfg, embed)


def show_result(record):
    result = record['result']
    st.caption(f'{result["mode"]} · {result["status"]} · {record.get("seconds", 0):.1f}초')
    source_text(result['answer'])
    for warning in record.get('warnings', []):
        st.warning(warning)
    sources = result['used_sources'] if result['mode'] == 'GMS 실제 생성' else record.get('sources', [])
    if not result['cited_numbers'] and result['mode'] == 'GMS 실제 생성':
        st.info('인용된 문서가 없어 답변을 보류했습니다.')
    for index, source in enumerate(sources, 1):
        number = source.get('number', index)
        with st.expander(f'[{number}] {source["title"]} · {source["source_type"]}'):
            st.caption(f'원문 수집: {source["collected_at"]} · 문단: {source.get("paragraph", "메타데이터")}')
            if source.get('event_company_name', '') == '' and source['source_type'].startswith('금감원'):
                st.caption('익명 업계 사례입니다. 선택 보험사의 실제 사건으로 연결하지 않습니다.')
            source_text(source['text'])
            source_button(source['url'], '공식 원문 확인 ↗')


def rag_view(insurers, cases):
    from .views import company_filter
    page_intro('GROUNDED AI WORKSPACE', '공시와 사례를 근거로 질문하세요.',
        '선택 회사·분기의 수치와 업계 공개 사례를 구분해 확인하고, 검토 방향을 정리합니다.')
    cfg = settings()
    st.caption('자료 검토 지원 기능입니다. 개별 사건의 지급·법적 결과를 확정하거나 전문가의 판단을 대신하지 않습니다.')
    tabs = st.tabs(['회사·분기 질문', '조건으로 공시 찾기'], key='rag_active_tab', on_change='rerun')
    with tabs[0]:
        context = company_filter(insurers)
        catalog = items(insurers)
        item = next(i for i in catalog if i['company'] == context['company'] and i['period'] == context['period'])
        a, b, c = st.columns([1, 1, 1.4])
        a.metric('실제 공시 항목', f'{len(catalog)}개')
        b.metric('GMS 키', '입력됨' if key_configured() else '미입력')
        with c:
            initialize = st.button('메타데이터 색인 준비·확인', key='rag_prepare', width='stretch')
        if initialize:
            with st.status('실제 로컬 임베딩 모델과 DB를 준비합니다.', expanded=True) as progress:
                try:
                    store = resources(fingerprint(cfg))
                    store.index_items(catalog)
                    st.session_state['rag_ready_signature'] = fingerprint(cfg)
                    progress.update(label=f'메타데이터 {store.meta.count()}개 색인 확인 완료', state='complete')
                except Exception:
                    progress.update(label='색인 준비 실패', state='error')
                    st.error('로컬 모델·DB를 준비하지 못했습니다. 설치 상태와 모델 다운로드 네트워크를 확인해 주세요.')
        if st.session_state.get('rag_ready_signature') != fingerprint(cfg):
            st.info('위의 ‘메타데이터 색인 준비·확인’을 먼저 누르세요. 설정을 변경하면 새 색인을 사용합니다.')
        if not key_configured():
            st.info('키가 없어도 실제 의미 검색 원문을 확인할 수 있습니다. 생성 답변은 실행하지 않습니다. .env 저장 후 다시 질문하세요.')
        conversations = st.session_state.setdefault('rag_conversations', {})
        messages = conversations.setdefault(item['item_id'], [])
        st.caption(f'이 대화의 범위: {item["title"]} · 회사·분기마다 대화가 분리됩니다.')
        for message in messages:
            with st.chat_message('user'):
                st.write(message['question'])
            with st.chat_message('assistant'):
                show_result(message)
        with st.form('rag_question_form', clear_on_submit=True):
            question = st.text_area('근거로 확인할 질문', placeholder='예: 민원 총건수와 유형별 분포를 알려줘. 추가 서류 요구 관련 사례에서는 무엇을 확인했어?', max_chars=2000, key='rag_question')
            submitted = st.form_submit_button('근거 검색 후 답변', width='stretch')
        if submitted:
            if not question.strip():
                st.warning('질문을 입력해 주세요.')
            else:
                with st.status('근거를 확인하고 있습니다.', expanded=True) as progress:
                    try:
                        from src.rag.pipeline import Pipeline
                        store = resources(fingerprint(cfg))
                        if not store.meta.get(ids=[item['item_id']])['ids']:
                            st.warning('선택 항목의 색인이 없습니다. 먼저 메타데이터 색인을 준비해 주세요.')
                            progress.update(label='색인 필요', state='error')
                        else:
                            start = time.perf_counter()
                            history = [{'question': m['question'], 'answer': m['result']['answer']} for m in messages[-2:]]
                            pipeline = Pipeline(cfg, store, cases, GMS(cfg) if key_configured() else None, progress=progress.write)
                            state = pipeline.run(item, question, history)
                            record = {'question': question, 'result': state['result'], 'sources': state['sources'],
                                'warnings': state['warnings'], 'seconds': time.perf_counter() - start}
                            messages.append(record)
                            progress.update(label='검색·인용 검사 완료', state='complete')
                            st.rerun()
                    except GMSError as error:
                        progress.update(label='GMS 요청을 완료하지 못했습니다.', state='error')
                        st.error(str(error))
                    except Exception:
                        progress.update(label='결과를 표시하지 않았습니다.', state='error')
                        st.error('수집·색인·응답 형식을 확인하지 못했습니다. 네트워크와 데이터 준비 상태를 확인한 뒤 다시 시도해 주세요.')
    with tabs[1]:
        st.caption('연도·분기·최소 건수는 정제 데이터로 확인합니다. 주제 검색 결과는 후보이며 의미 적합성을 검토해야 합니다.')
        query = st.text_input('자연어 조건', placeholder='예: 2026년 2분기 민원 100건 이상인 손해보험', key='rag_discovery_query')
        if st.button('공시 후보 찾기', key='rag_discover'):
            allowed = items(insurers)
            year = re.search(r'(20\d{2})년?', query)
            quarter = re.search(r'([1-4])\s*분기', query)
            minimum = re.search(r'(\d[\d,]*)\s*건\s*이상', query)
            for match, predicate in [
                (year, lambda i: i['period'].startswith(year.group(1)) if year else True),
                (quarter, lambda i: i['period'].endswith('Q' + quarter.group(1)) if quarter else True),
                (minimum, lambda i: i['total'] is not None and i['total'] >= int(minimum.group(1).replace(',', '')) if minimum else True)]:
                if match:
                    allowed = [i for i in allowed if predicate(i)]
            if '손해보험' in query or '생명보험' in query:
                sector = '손해보험' if '손해보험' in query else '생명보험'
                allowed = [i for i in allowed if i['sector'] == sector]
            named = [i for i in allowed if i['company'] in query]
            if named:
                allowed = named
            if not allowed:
                st.session_state['rag_discovery_results'] = []
            else:
                try:
                    store = resources(fingerprint(cfg))
                    store.index_items(items(insurers))
                    ids = store.discover(query, [i['item_id'] for i in allowed])
                    checked = False
                    if key_configured():
                        from src.rag.pipeline import validate_selection
                        from src.rag.prompts import SELECT
                        response = GMS(cfg).json(SELECT, {'question': query, 'candidates': [
                            {'id': i['item_id'], 'title': i['title'], 'service': i['sector'], 'body': i['text']} for i in allowed if i['item_id'] in ids]})
                        ids = validate_selection(response, set(ids))
                        checked = True
                    st.session_state['rag_discovery_results'] = [next(i for i in allowed if i['item_id'] == ident) | {'gms_candidate_checked': checked} for ident in ids]
                except Exception:
                    st.error('의미 검색 색인을 준비하지 못했습니다.')
        for found in st.session_state.get('rag_discovery_results', []):
            with st.container(border=True):
                st.write(found['title'])
                check_label='GMS 후보 선별 확인' if found.get('gms_candidate_checked') else '의미 후보·생성 검증 전'
                st.caption(f'{found["sector"]} · 민원 {found["total"]}건 · 조건 일치 / {check_label}')
                def choose(selected=found):
                    st.session_state['company'] = selected['company']
                    st.session_state['company_period'] = selected['period']
                    st.session_state['insurer_sector'] = selected['sector']
                    st.session_state['rag_active_tab'] = '회사·분기 질문'
                    for key in ('_company_ui', '_company_period_ui', '_insurer_sector_ui'):
                        st.session_state.pop(key, None)
                st.button('이 공시로 질문하기 ↑', key='rag_open_' + found['item_id'], on_click=choose)
