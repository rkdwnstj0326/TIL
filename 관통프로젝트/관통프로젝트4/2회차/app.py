"""FinVOC 화면 진입점. 통계·검색 로직과 UI 표현을 모듈로 분리한다."""
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from src.collection.client import ROOT
from src.ui.components import inject_theme, brand_header
from src.ui.views import overview, analysis, cases_view, data_management
from src.ui.rag_view import rag_view

st.set_page_config(page_title='FinVOC Korea · 금융민원 워크벤치',page_icon='◈',layout='wide')
inject_theme()


@st.cache_data(show_spinner=False)
def load_data(file_versions):
    # 파일의 수정 시각을 캐시 키로 써서 데이터 갱신 후 예전 화면이 남지 않게 한다.
    def read(name):
        return json.loads((ROOT/name).read_text('utf-8'))
    expanded=(ROOT/'data/processed/insurer_stats_all.json').exists() and (ROOT/'reports/insurer_expansion.json').exists()
    historical=(ROOT/'data/processed/insurer_stats_history.json').exists() and (ROOT/'reports/insurer_history.json').exists()
    audit=read('reports/phase0_audit.json')
    if expanded:
        expansion=read('reports/insurer_expansion.json')
        audit['insurer_expansion']=expansion
        audit['statistics']['checks']+=expansion['checks']
        audit['integrity']['checked_files']+=len(expansion['sources'])
        audit['generated_at']=expansion['generated_at']
    if historical:
        history=read('reports/insurer_history.json')
        audit['insurer_history']=history
        audit['statistics']['checks']+=history['checks']
        audit['integrity']['checked_files']+=len(history['sources'])
        audit['generated_at']=history['generated_at']
    return (read('data/processed/sector_stats.json'),
            read('data/processed/insurer_stats_history.json' if historical else 'data/processed/insurer_stats_all.json' if expanded else 'data/processed/insurer_stats.json'),
            read('data/private/cases.json'),audit)


try:
    paths=['data/processed/sector_stats.json','data/processed/insurer_stats.json',
           'data/private/cases.json','reports/phase0_audit.json']
    paths += ['data/processed/insurer_stats_all.json','reports/insurer_expansion.json','data/metadata/insurer_registry.json']
    paths += ['data/processed/insurer_stats_history.json','reports/insurer_history.json','data/metadata/insurer_registry_history.json']
    versions=tuple((ROOT/path).stat().st_mtime_ns if (ROOT/path).exists() else 0 for path in paths)
    sectors,insurers,cases,audit=load_data(versions)
except (FileNotFoundError,json.JSONDecodeError):
    brand_header()
    st.title('분석 자료를 준비해 주세요.')
    st.info('README의 데이터 준비 명령을 실행하면 공식 통계와 공개 사례를 확인할 수 있습니다.')
    st.stop()

st.session_state.setdefault('workspace','업무 개요')
st.session_state.setdefault('company','하나손해보험')
st.session_state.setdefault('search_query','')
st.session_state.setdefault('search_group','전체')
brand_header()


with st.container(key='main_nav'):
    section=st.segmented_control('작업 공간',['업무 개요','민원 분석','사례 탐색','근거 기반 AI','자료 관리'],
                                 key='workspace',width='stretch',label_visibility='collapsed',required=True)

if section=='업무 개요':
    overview(insurers)
elif section=='민원 분석':
    analysis(sectors,insurers)
elif section=='사례 탐색':
    cases_view(cases)
elif section=='근거 기반 AI':
    rag_view(insurers,cases)
else:
    data_management(sectors,insurers,cases,audit)

checked=datetime.fromisoformat(audit['generated_at']).astimezone(ZoneInfo('Asia/Seoul')).strftime('%Y.%m.%d')
st.markdown(f'<div class="footerline">FinVOC Korea · 공식 자료 기반 개인 연구용 워크벤치　|　자료 확인 {checked}<br>통계와 익명 업계 사례의 집계 범위는 다릅니다. 근거 기반 AI에서 실제 GMS 생성과 원문 발췌를 구분합니다.</div>',unsafe_allow_html=True)
