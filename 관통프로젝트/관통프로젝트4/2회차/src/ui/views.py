"""업무 흐름: 공시 현황 확인 → 검토 질문 선택 → 업계 공개 사례 원문 확인."""
from html import escape
import json
from src.collection.client import ROOT
import pandas as pd
import streamlit as st
from src.analysis.case_search import CaseSearch
from src.analysis.dashboard import period_label, snapshot, review_question
from src.analysis.complaint_trends import growth
from .components import (badge, card_heading, channel_chart, company_metrics, context_bar,
                         distribution_chart, page_intro, source_button, source_text)


def navigate(section,query=None,group='전체'):
    st.session_state['workspace']=section
    if query is not None:
        st.session_state['search_query']=query
        st.session_state['search_group']=group
        st.session_state['search_run_pending']=True


def company_filter(insurers):
    registry_path=ROOT/('data/metadata/insurer_registry_history.json' if (ROOT/'data/metadata/insurer_registry_history.json').exists() else 'data/metadata/insurer_registry.json')
    registry=json.loads(registry_path.read_text('utf-8')) if registry_path.exists() else {}
    names=sorted({r['company'] for r in insurers})
    sector_of=lambda name:registry.get(name,{}).get('sector','손해보험')
    all_periods=sorted({r['period'] for r in insurers})
    st.caption(f'과거 공시 포함 {len(names)}개사 · {period_label(all_periods[0])}~{period_label(all_periods[-1])} · 회사별 제공 기간이 다릅니다.')
    with st.container(border=True,key='company_filter'):
        sector_col,left,right=st.columns([1,2.2,1])
        with sector_col:
            sector_options=[s for s in ['손해보험','생명보험','재보험'] if any(sector_of(n)==s for n in names)]
            st.session_state['_insurer_sector_ui']=st.session_state.get('insurer_sector','손해보험')
            def keep_sector():
                st.session_state['insurer_sector']=st.session_state['_insurer_sector_ui']
            sector=st.selectbox('보험 업권',sector_options,key='_insurer_sector_ui',on_change=keep_sector)
        candidates=[n for n in names if sector_of(n)==sector]
        if not candidates:
            st.info('이 업권의 공시 자료는 아직 없습니다.')
            st.stop()
        if st.session_state.get('company') not in candidates:
            st.session_state['company']=candidates[0]
        with left:
            st.session_state['_company_ui']=st.session_state['company']
            def keep_company():
                st.session_state['company']=st.session_state['_company_ui']
            company=st.selectbox('분석 보험사',candidates,key='_company_ui',on_change=keep_company)
        with right:
            periods=sorted({r['period'] for r in insurers if r['company']==company})
            if st.session_state.get('company_period') not in periods:
                st.session_state['company_period']=periods[-1]
            st.session_state['_company_period_ui']=st.session_state['company_period']
            def keep_period():
                st.session_state['company_period']=st.session_state['_company_period_ui']
            period=st.selectbox('공시 기간',periods,format_func=period_label,key='_company_period_ui',on_change=keep_period)
    data=snapshot(insurers,company,period)
    data['registry']=registry.get(company,{})
    if any(r['axis']=='상품' and '미확인' in r.get('denominator_scope','') for r in data['rows']):
        data['registry']['denominator']='해당기간 회사 전체 환산단위는 10만건당. 상품 상세 분모(상품별/전체)는 해당 협회 표에서 미확인.'
    if data['registry'].get('caution'):
        st.caption(data['registry']['caution'])
    if data.get('comparison_blocked'):
        st.warning('2024년 2분기 공시기준 개선 전후라 전분기 증감을 계산하지 않습니다. 각 분기의 원문 수치만 확인해 주세요.')
    if company=='교보생명':
        st.caption('교보생명은 현재 2026년 1·2분기만 확보했습니다. 손보 과거 자료를 생보에 복사하지 않습니다.')
    return data


def company_source(data):
    st.caption('출처: 선택 보험사 민원 공시 · 같은 민원을 유형·접수경로·상품으로 나눈 표입니다. 분류축을 합산하지 않습니다.')
    source_button(data['source_url'])
    registry=data.get('registry',{})
    if registry:
        st.write(registry['denominator'])
        st.write(registry['definition_status'])
        st.write(registry['caution'])


def overview(insurers):
    page_intro('COMPLAINT INSIGHT WORKSPACE','민원 현황과 관련 사례를 한눈에.',
               '어떤 민원이 많은지 확인하고, 유사 쟁점에서 기관이 검토한 근거를 찾아보세요.')
    data=company_filter(insurers)
    if data['total'] is None:
        st.info('선택한 기간의 공시 자료가 없습니다.')
        return
    context_bar(data)
    company_metrics(data)
    st.write('')
    left,right=st.columns([1.25,1])
    with left,st.container(border=True,key='card_type_distribution'):
        card_heading('어떤 유형의 민원이 많을까요?','선택 회사·분기의 유형별 공시 건수')
        distribution_chart(data['types'])
    with right,st.container(border=True,key='card_channel_distribution'):
        card_heading('민원은 어디로 접수되었을까요?','자체민원과 타기관 이첩·사실조회 민원 구성')
        channel_chart(data['rows'],data['total'])
    st.write('')
    card_heading('우선 살펴볼 민원 유형','이 회사의 공시 건수 순입니다. 아래 질문은 담당자가 확인할 검토 주제입니다.')
    if not data['top_types']:
        st.info('공시 민원이 0건이라 유형별 검토 순서를 제시하지 않습니다.')
    else:
        for i,(column,row) in enumerate(zip(st.columns(len(data['top_types'])),data['top_types'],strict=True),1):
            with column,st.container(border=True,key=f'card_priority_{i}'):
                share=row['count']/data['total']*100 if data['total'] else 0
                st.markdown(f'<div class="rankrow"><span class="ranknum">{i:02}</span><div><div class="rankname">{escape(row["category"])}</div><div class="rankdesc">전체 민원의 {share:.1f}%</div></div><span class="rankvalue">{row["count"]:,}건</span></div>',unsafe_allow_html=True)
                question,query=review_question(row['category'])
                st.markdown(f'<div class="nextquestion">{escape(question)}</div>',unsafe_allow_html=True)
                st.button('관련 사례 검토 →',key=f'review_{i}',on_click=navigate,args=('사례 탐색',query),width='stretch')
    st.markdown('<div class="sectionnote">관련 사례는 금융감독원이 공개한 업계 사례입니다. 선택 보험사에서 발생한 사건으로 연결하지 않습니다.</div>',unsafe_allow_html=True)
    with st.expander('수치 해석과 공시 출처'):
        st.write('보상 유형의 비중은 보험금 부지급률이 아닙니다. 환산건수의 분모는 분기말 보유계약입니다. 회사별 상품 구성과 세부 제외 항목은 다를 수 있습니다.')
        company_source(data)


def analysis(sectors,insurers):
    page_intro('DISCLOSURE ANALYTICS','같은 기준으로 민원 흐름을 읽습니다.',
               '회사 공시는 분기별로, 금감원 통계는 전년 동기 기준으로 살펴봅니다.')
    level=st.radio('분석 자료',['보험사 공시','금감원 동향'],horizontal=True,key='analysis_level')
    if level=='보험사 공시':
        data=company_filter(insurers)
        if data['total'] is None:
            st.info('이 기간의 공시가 없습니다.')
            return
        context_bar(data)
        company_metrics(data)
        st.write('')
        with st.container(border=True,key='card_analysis_chart'):
            a,b=st.columns([1.6,1])
            with a:
                axis=st.radio('민원 분류',['유형','접수경로','상품'],horizontal=True)
            with b:
                measurement=st.selectbox('표시 지표',['민원 건수','보유계약 10만건당'])
            selected=[r for r in data['rows'] if r['axis']==axis and r['category']!='합계']
            if measurement!='민원 건수' and axis=='상품':
                st.caption(data.get('registry',{}).get('denominator','상품별 분모는 출처에서 확인해 주세요.'))
                st.caption('상세 분모 미확인 자료의 상품간 환산값 비교는 보류합니다. 환산값은 합산하지 않으며, 빈 값은 0이 아닙니다.')
            if measurement!='민원 건수' and axis=='상품' and '미확인' in data.get('registry',{}).get('denominator',''):
                st.info('상품 환산건수의 상세 분모가 미확인이라 비교 차트는 표시하지 않습니다. 아래 표에서 원문 수치만 확인할 수 있습니다.')
            else:
                distribution_chart(selected,'count' if measurement=='민원 건수' else 'rate_per_100k')
        lower_left,lower_right=st.columns([1.15,1])
        with lower_left,st.container(border=True,key='card_source_values'):
            card_heading('원문 수치 확인',f"{period_label(data['period'])} · {axis}별 공시")
            st.dataframe(pd.DataFrame([{'분류':r['category'],'민원(건)':r['count'],
                                       '보유계약 10만건당':r['rate_per_100k']} for r in selected]),
                         hide_index=True,width='stretch')
            st.caption('빈 환산건수는 원문에서 산정하지 않은 값입니다.')
        with lower_right,st.container(border=True,key='card_quarter_trend'):
            card_heading('분기별 공시 민원 추이','선택 회사의 연속 분기 · 단위: 건')
            available=sorted({r['period'] for r in insurers if r['company']==data['company']})
            first=int(available[0][:4])*4+int(available[0][-1])-1
            last=int(available[-1][:4])*4+int(available[-1][-1])-1
            periods=[f'{p//4}Q{p%4+1}' for p in range(first,last+1)]
            trend=[{'category':period_label(p),'count':snapshot(insurers,data['company'],p)['total'],
                    '공시기준':snapshot(insurers,data['company'],p)['definition_regime']} for p in periods]
            # 추세는 기간 순서를 보존한다. 건수로 정렬하는 분포 차트와 구분한다.
            import plotly.express as px
            from .components import base_chart
            fig=base_chart(px.line(pd.DataFrame(trend),x='category',y='count',color='공시기준',markers=True,
                color_discrete_sequence=['#0b9396','#a3adb6']),height=230)
            fig.update_traces(marker_size=8,connectgaps=False)
            fig.update_xaxes(title='',showgrid=False)
            fig.update_yaxes(title='',rangemode='tozero',gridcolor='#edf2f6')
            st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
            st.caption('기준 변경 전후의 선은 연결하지 않습니다. 빠진 분기는 누락으로 남기며 0건으로 보간하지 않습니다.')
        with st.expander('집계 기준과 출처 행'):
            st.write('세 분류축은 같은 민원의 다른 구분이므로 더하지 않습니다. 회사 규모·상품 구성·세부 제외 문구를 보정한 순위는 제공하지 않습니다.')
            for row in selected:
                source_text(row['source_row'])
            company_source(data)
    else:
        with st.container(border=True,key='card_sector_filter'):
            a,b=st.columns([1.5,1])
            with a:
                sector=st.selectbox('금융 권역',['보험','생명보험','손해보험','금융민원','은행','중소서민','금융투자'])
            with b:
                kind=st.selectbox('비교 기간',['상반기끼리 비교','연간끼리 비교'])
        periods=['2025H1','2026H1'] if kind=='상반기끼리 비교' else ['2024','2025']
        previous,current=sorted([r for r in sectors if r['sector']==sector and r['period'] in periods],key=lambda r:r['period'])
        a,b,c=st.columns(3)
        a.metric(period_label(previous['period']),f"{previous['count']:,}건")
        b.metric(period_label(current['period']),f"{current['count']:,}건")
        c.metric('전년 동기 대비',f"{growth(previous['count'],current['count']):+.1f}%")
        with st.container(border=True,key='card_sector_chart'):
            card_heading(f'{sector} 민원 접수 추이','접수일 기준 · 처리건수와 구분')
            distribution_chart([{'category':period_label(r['period']),'count':r['count']} for r in [previous,current]])
        st.caption('금감원 2026년 상반기 보고서 PDF 9쪽의 비교 열입니다. 연간과 반기를 직접 증감 비교하지 않습니다.')
        source_button(current['source_url'],'금감원 통계 원문 · KDI 제공 ↗')


def run_search(cases,query,group):
    corpus=cases if group=='전체' else [c for c in cases if c['service'].split('(')[0]==group]
    st.session_state['finvoc_hits']=CaseSearch(corpus).search(query,5)
    st.session_state['last_query']=query
    st.session_state['last_group']=group
    hits=st.session_state['finvoc_hits']
    st.session_state['selected_case']=hits[0]['case_id'] if hits else None


def select_case(case_id):
    st.session_state['selected_case']=case_id


def cases_view(cases):
    page_intro('EVIDENCE EXPLORER','유사 쟁점에서, 검토 근거를 찾습니다.',
               '기관이 공개한 민원 내용과 처리 결과를 원문으로 확인하세요.')
    st.markdown(f'{badge("원문 검색")}{badge("공식 공개 사례",True)}<span class="smallmeta">검색한 자료를 발췌합니다. AI 생성 답변이나 보상 가능성 판정이 아닙니다.</span>',unsafe_allow_html=True)
    st.write('')
    with st.form('case_search'):
        a,b,c=st.columns([3,1.2,.9],vertical_alignment='bottom')
        with a:
            query=st.text_input('검토할 고객 문제',placeholder='예: 보험금 청구 시 영수증 외 추가 서류를 요구한 사례',key='search_query',max_chars=2000)
        with b:
            group=st.selectbox('보험 서비스',['전체']+sorted({c['service'].split('(')[0] for c in cases}),key='search_group')
        with c:
            submitted=st.form_submit_button('관련 사례 검색',type='primary',width='stretch')
    examples=[('청구 서류','보험금 청구 진료비 영수증 추가 서류','실손보험'),
              ('백내장 수술','백내장 다초점 인공수정체 실손 보상','실손보험'),
              ('설명 의무','유니버셜 종신보험 설명의무 해피콜','전체'),
              ('계약 부활','보험료 연체 계약 해지 부활','전체')]
    for column,(label,example,service) in zip(st.columns(4),examples,strict=True):
        column.button(label,key='example_'+label,on_click=navigate,args=('사례 탐색',example,service),width='stretch')
    pending=st.session_state.pop('search_run_pending',False)
    if submitted or pending:
        run_search(cases,query.strip(),group)
    if 'finvoc_hits' not in st.session_state:
        with st.container(border=True,key='card_search_empty'):
            st.markdown('<div class="emptytitle">어떤 쟁점을 검토하고 싶으신가요?</div><div class="emptybody">고객 문제를 입력하거나 위의 예시를 선택해 보세요.<br>관련 사례 목록과 기관이 정리한 판단 근거를 나란히 보여드립니다.</div>',unsafe_allow_html=True)
        return
    hits=st.session_state['finvoc_hits']
    st.markdown(f'<div class="resultcount">검색어 <b>{escape(st.session_state.get("last_query","")) or "(비어 있음)"}</b> · {escape(st.session_state.get("last_group","전체"))} · 검색 후보 {len(hits)}개</div>',unsafe_allow_html=True)
    if not hits:
        st.warning('관련 사례를 찾지 못했습니다. 더 짧은 쟁점 단어나 다른 보험 서비스로 검색해 주세요.')
        st.caption('자료에 없는 내용을 만들어 답하지 않습니다. 현재 검색은 단어·문자 일치 기반이라 같은 뜻의 다른 표현을 놓칠 수 있습니다.')
        return
    left,right=st.columns([1,1.55])
    with left:
        card_heading('검토할 사례 후보','검색어가 겹치는 자료입니다. 선택해 원문을 확인하세요.')
        for i,hit in enumerate(hits,1):
            selected=st.session_state.get('selected_case')==hit['case_id']
            with st.container(border=True,key='case_hit_'+hit['case_id']):
                st.caption(f'{i:02} · {hit["service"]}')
                st.button(hit['title'],key='open_'+hit['case_id'],type='primary' if selected else 'secondary',
                          on_click=select_case,args=(hit['case_id'],),width='stretch')
                st.caption('게시 '+hit['published_date'])
        with st.expander('검색 방식과 중복 처리'):
            st.caption('이 화면은 문자 TF-IDF 기준선입니다. 의미 검색과 GMS 생성은 ‘근거 기반 AI’에서 사용하세요. 동일 제목은 최신 게시본을 우선 검색하며 원본은 보존합니다. 점수는 보상 가능성이 아닙니다.')
            st.dataframe(pd.DataFrame([{'문서':h['case_id'],'문자 유사도':h['score']} for h in hits]),hide_index=True,width='stretch')
    with right,st.container(border=True,key='card_case_detail'):
        selected=next((h for h in hits if h['case_id']==st.session_state.get('selected_case')),hits[0])
        case=next(c for c in cases if c['case_id']==selected['case_id'])
        number=next(i for i,h in enumerate(hits,1) if h['case_id']==case['case_id'])
        st.markdown(badge('근거 '+str(number))+badge('금융감독원',True),unsafe_allow_html=True)
        st.markdown(f'<div class="detailtitle">{escape(case["title"])}</div>',unsafe_allow_html=True)
        st.caption(f"게시 {case['published_date']} · 수집 {case['retrieved_at'][:10]} · 결정일은 별도 미확인")
        source_button(case['source_url'],'금융감독원 원문 확인 ↗')
        detail_tabs=st.tabs(['쟁점·처리 근거','민원 내용','소비자 유의사항'])
        with detail_tabs[0]:
            card_heading('기관이 정리한 쟁점')
            source_text(case['issues'])
            card_heading('판단·처리결과 원문')
            source_text(case['resolution_text'])
            st.caption('당시의 개별 사실관계와 약관에 관한 처리 결과입니다. 모든 계약의 현재 보상 기준으로 일반화할 수 없습니다.')
        with detail_tabs[1]:
            source_text(case['facts'])
            st.caption('소비자·회사 주장이 별도 구획으로 확정되지 않은 자료는 분리해서 추정하지 않습니다.')
        with detail_tabs[2]:
            source_text(case['caution'])
        with st.expander('검색에 사용한 인용 문단'):
            for paragraph in selected['excerpts']:
                st.caption(f"근거 [{number}] · 추출 문단 {paragraph['paragraph']} · {paragraph['section']}")
                source_text(paragraph['text'])
    st.markdown('<div class="sectionnote">공개 업계 사례를 검색합니다. 특정 보험사의 사건으로 연결하지 않으며 게시일을 결정일로 보지 않습니다.</div>',unsafe_allow_html=True)


def data_management(sectors,insurers,cases,audit):
    page_intro('DATA & PROVENANCE','자료의 출처와 범위를 확인합니다.',
               '분석 수치의 근거, 데이터 품질, 아직 확인하지 않은 내용을 구분해 기록합니다.')
    a,b,c,d=st.columns(4)
    a.metric('공식 통계·공시',f'{len(sectors)+len(insurers)}개 관측값')
    b.metric('공개 사례 문서',f'{len(cases)}개')
    c.metric('원본 파일 확인',f"{audit['integrity']['checked_files']}개")
    checks=audit['statistics']['checks']+audit['cross_source_checks']
    d.metric('통계·출처 검사',f"{sum(c['passed'] for c in checks)}/{len(checks)}")
    tabs=st.tabs(['자료 목록','검증 기록','집계 기준·이용 범위'])
    with tabs[0]:
        sources=[
            ('금감원 금융민원 동향','2026년 상반기 · KDI 공식 제공본','https://eiec.kdi.re.kr/policy/materialView.do?num=287509'),
            ('금감원 금융민원 동향','2025년 연간 · KDI 공식 제공본','https://eiec.kdi.re.kr/policy/materialView.do?num=279797'),
            ('하나손해보험 민원 공시','2026년 1·2분기 · 2025년 4분기 비교값 포함','https://www.hanainsure.co.kr/w/consumer/finaneConsumer/complainDisclosures'),
            ('신한EZ손해보험 민원 공시','2026년 1·2분기','https://www.shinhanez.co.kr/static/cpo/CPO600M0154.html'),
            ('금감원 공개 분쟁조정사례',f'{len(cases)}개 게시 문서 · 개별 실제 사건 수는 미확정','https://www.fss.or.kr/fss/job/fncCnflCase/list.do?menuNo=201195'),
            ('금감원 저작권 정책','개인 교육·연구 검토와 외부 재배포를 구분','https://www.fss.or.kr/fss/main/contents.do?menuNo=200701')]
        expansion=audit.get('insurer_expansion')
        history=audit.get('insurer_history')
        if history:
            st.info(f"과거 공시 확장: {history['company_quarter_items']}개 회사·분기 / {history['observations']}개 관측값. 2024Q1~2026Q2. 회사별 기간과 원문 기준은 다릅니다.")
            for excluded in history['excluded']:
                st.warning(f"{excluded['company']} {excluded['period']}: {excluded['reason']}")
            sources.extend([('손해보험협회 과거 공시',source['source_id'],source['source_page']) for source in history['sources']])
        if expansion:
            sources.extend([
                ('손해보험협회 통합 민원 공시','17개 손해보험사 · 2026년 1·2분기 · 기존 2개사 직접 공시와 52항목 대조','https://consumer.knia.or.kr/m/disclosure/item/01.do'),
                ('교보생명 민원 공시','2026년 1·2분기 · 생명보험 분류 및 즉시연금 제외조건 유지','https://www.kyobo.com/dgt/web/customer/customer-proposal/cval-prcn'),
                ('손해보험협회 공식 작성 매뉴얼','2024-06-30 제정 · 공시대상·제외조건·분류를 본문에서 확인','https://consumer.knia.or.kr/common/filedown.do?fileName=minwon')])
            st.caption(f"현재 {expansion['company_count']}개사 · 공통 비교 시점 2026년 2분기. 기존 65개 관측값은 별도 보존했습니다.")
        for i in range(0,len(sources),2):
            for j,(column,(name,period,url)) in enumerate(zip(st.columns(len(sources[i:i+2])),sources[i:i+2],strict=True)):
                with column,st.container(border=True,key='card_data_source_'+str(i+j)):
                    card_heading(name,period)
                    source_button(url,'공식 출처 확인 ↗')
    with tabs[1]:
        st.dataframe(pd.DataFrame([
            {'검증 항목':'본문 구조','확인 결과':f'{len(cases)}개 문서에서 민원내용·쟁점·처리결과 추출'},
            {'검증 항목':'중복 후보','확인 결과':'동일 제목 1그룹 2게시본 · 실제 사건 동일성 미확인'},
            {'검증 항목':'원본 무결성','확인 결과':f"{audit['integrity']['checked_files']}개 SHA-256 일치"},
            {'검증 항목':'반복 캐시 조회','확인 결과':f"HTTP 재호출 {audit['cache_repeat']['http_calls']}회"},
            {'검증 항목':'숫자 정합성','확인 결과':f"통계 {len(audit['statistics']['checks'])}개 · PDF/HTML {len(audit['cross_source_checks'])}개 확인"},
            {'검증 항목':'검색·인용 스모크','확인 결과':'5문항 확인 · 독립 성능평가 아님'},
            {'검증 항목':'의미 검색·AI 생성','확인 결과':'근거 기반 AI 화면 제공 · 실제 결과는 reports/rag_comparison.json 참조'},
            {'검증 항목':'검색 정확도','확인 결과':'독립 30문항 정답셋 평가 전'},
        ]),hide_index=True,width='stretch')
        st.caption('원문 70개에 식별정보 유사 정규식을 적용했으나 완전한 익명화를 보증하지 않습니다. 외부 공개 전 개별 검수가 필요합니다.')
        if audit.get('insurer_expansion'):
            expansion=audit['insurer_expansion']
            st.caption(f"보험사 확장 검사 {len(expansion['checks'])}개 통과 · 출처 {len(expansion['sources'])}개 재조회 HTTP {expansion['cache_repeat']['http_calls']}회. 위 통계 검사에는 원래 Phase 0 검사와 확장 검사를 함께 표시합니다.")
            with st.expander('회사별 분기·분모·분류 기준 확인표'):
                registry=json.loads((ROOT/('data/metadata/insurer_registry_history.json' if history else 'data/metadata/insurer_registry.json')).read_text('utf-8'))
                st.dataframe(pd.DataFrame([{'보험사':r['company'],'업권':r['sector'],
                    '기간':', '.join(r['periods']),'분모':r['denominator'],
                    '유형':', '.join(r['categories']),'주의사항':r['caution']} for r in registry.values()]),
                    hide_index=True,width='stretch')
                for r in expansion['not_included']:
                    st.caption(r['company']+' · '+r['reason'])
    with tabs[2]:
        with st.container(border=True,key='card_terms'):
            card_heading('공시 숫자와 사례 문서는 서로 다른 자료입니다.')
            st.write('사례 문서 수를 전체 민원 발생 건수·발생률로 해석하거나, 익명 사례를 특정 회사 사건으로 연결하지 않습니다. 같은 민원의 분류축도 합산하지 않습니다.')
            card_heading('비교 기간과 분모를 유지합니다.')
            st.write('연간과 반기를 직접 비교하지 않습니다. 환산건수는 회사/상품별 분기말 계약 수를 기준으로 하며, 세부 제외 문구가 다른 회사의 우열 순위를 만들지 않습니다.')
            st.write('협회 새 15개사의 상품표 상세 분모는 미확인입니다. 해당 상품 환산값의 비교를 보류합니다. 공식 작성 매뉴얼의 자율조정 성립·합의취하·임의철회·B2B·소송관련 제외조건도 확인했습니다.')
            card_heading('현재는 개인 교육·연구용 로컬 검토판입니다.')
            st.write('공식 출처라도 자유로운 원문 재배포가 자동 허용되지는 않습니다. 공개 배포·GitHub 원문 업로드 조건은 확인 전이며 현재 진행하지 않았습니다.')
            st.caption('한국소비자원은 robots.txt에서 자동 수집을 금지해 이번 자료에 포함하지 않았습니다. 소비자24 접근 제한도 우회하지 않았습니다.')
