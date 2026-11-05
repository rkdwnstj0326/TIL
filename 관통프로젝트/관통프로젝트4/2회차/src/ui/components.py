"""공통 디자인과 차트. 기관 원문은 HTML 이스케이프 후 자료로만 표시한다."""
from html import escape
from pathlib import Path
from urllib.parse import urlparse
import pandas as pd
import plotly.express as px
import streamlit as st
from src.analysis.dashboard import period_label

INK='#19394e'
TEAL='#0b9396'
COLORS=['#143f56','#0b9396','#78bac1','#bbcdd7']


def inject_theme():
    css=Path(__file__).with_name('theme.css').read_text('utf-8')
    st.markdown('<style>'+css+'</style>',unsafe_allow_html=True)


def brand_header():
    st.markdown('''<div class="brandbar"><div class="brandgroup">
    <div class="brandmark"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 22 12 12 22 2 12Z" fill="none" stroke="#70d3ca" stroke-width="1.5"/><path d="m7 14 4-5 3 3 4-5" fill="none" stroke="white" stroke-width="1.6"/></svg></div>
    <span class="brandname">FinVOC Korea</span><span class="brandcontext">금융소비자보호 워크벤치</span></div>
    <span class="brandstatus">● 공식 자료 · 근거 기반 AI</span></div>''',unsafe_allow_html=True)


def page_intro(kicker,title,description):
    st.markdown(f'<div class="eyebrow">{escape(kicker)}</div>',unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="intro">{escape(description)}</div>',unsafe_allow_html=True)


def card_heading(title,subtitle=None):
    st.markdown(f'<div class="sectionlabel">{escape(title)}</div>',unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="sectionnote">{escape(subtitle)}</div>',unsafe_allow_html=True)


def badge(text,muted=False):
    return f'<span class="tag {"mutedtag" if muted else ""}">{escape(str(text))}</span>'


def source_text(text):
    # 원문의 태그·스크립트·링크 표현이 실행되지 않도록 반드시 이스케이프한다.
    st.markdown(f'<div class="sourcebox">{escape(text or "명시되지 않음")}</div>',unsafe_allow_html=True)


def source_button(url,label='공식 공시 원문 ↗'):
    if url:
        st.link_button(label,url)


def base_chart(fig,height=250):
    fig.update_layout(height=height,margin=dict(l=8,r=40,t=15,b=20),
                      paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(family='Malgun Gothic, sans-serif',size=11,color='#647d8e'),
                      showlegend=False,dragmode=False)
    fig.update_xaxes(fixedrange=True,zeroline=False)
    fig.update_yaxes(fixedrange=True,zeroline=False)
    return fig


def distribution_chart(rows,metric='count'):
    if not rows:
        st.info('이 분류의 공시 자료가 없습니다.')
        return
    df=pd.DataFrame(rows).sort_values('count',ascending=False)
    if metric=='rate_per_100k':
        df=df[df['rate_per_100k'].notna()]
        if df.empty:
            st.info('이 항목의 환산건수는 원문에 없습니다.')
            return
    color={name:COLORS[i%len(COLORS)] for i,name in enumerate(df['category'])}
    fig=px.bar(df,x=metric,y='category',orientation='h',color='category',color_discrete_map=color,
               text=metric,labels={'category':'','count':'민원(건)','rate_per_100k':'보유계약 10만건당'})
    fig=base_chart(fig)
    suffix='건' if metric=='count' else ''
    fig.update_traces(texttemplate=f'%{{x:,.0f}}{suffix}' if metric=='count' else '%{x:.2f}',
                      textposition='outside',cliponaxis=False,width=.48,hovertemplate='%{y}<br>%{x}<extra></extra>')
    fig.update_yaxes(autorange='reversed',categoryorder='array',categoryarray=df['category'].tolist(),
                     title='',showgrid=False,tickfont=dict(size=12,color=INK))
    fig.update_xaxes(title='',showgrid=True,gridcolor='#edf2f6',range=[0,max(df[metric].max()*1.25,1)],
                     tickformat=',d' if metric=='count' else '.1f')
    st.plotly_chart(fig,width='stretch',config={'displayModeBar':False,'responsive':True})


def channel_chart(rows,total):
    selected=[r for r in rows if r['axis']=='접수경로' and r['category']!='합계' and r['count']>0]
    if not selected:
        st.info('접수경로 자료가 없습니다.')
        return
    df=pd.DataFrame(selected)
    fig=px.pie(df,names='category',values='count',hole=.73,
               color='category',color_discrete_map={'자체민원':'#8bc7ca','대외민원':'#153f56'})
    fig=base_chart(fig)
    fig.update_traces(textinfo='none',hovertemplate='%{label}<br>%{value}건 · %{percent}<extra></extra>',
                      marker=dict(line=dict(color='white',width=3)),sort=False)
    fig.update_layout(showlegend=True,legend=dict(orientation='h',x=.5,xanchor='center',y=-.06),
                      margin=dict(l=10,r=10,t=10,b=30),
                      annotations=[dict(text=f'<b>{total:,}</b>',x=.5,y=.54,showarrow=False,
                                        font=dict(size=29,color=INK)),
                                   dict(text='공시 민원',x=.5,y=.39,showarrow=False,font=dict(size=11,color='#7791a2'))])
    st.plotly_chart(fig,width='stretch',config={'displayModeBar':False,'responsive':True})


def context_bar(data):
    url=data.get('source_url') or ''
    link=(f'<a class="contextsource" href="{escape(url,quote=True)}" target="_blank" rel="noopener noreferrer">공식 공시 원문 ↗</a>'
          if urlparse(url).scheme=='https' else '')
    st.markdown(f'<div class="contextline"><strong>{escape(data["company"])}</strong>　'
                f'{badge(period_label(data["period"]),True)} {badge(data.get("registry",{}).get("sector","손해보험")+" 공시",True)}{link}</div>',unsafe_allow_html=True)


def company_metrics(data):
    columns=st.columns(4)
    columns[0].metric('공시 민원',f"{data['total']:,}건",help='선택한 회사·분기의 자체민원과 대외민원 합계입니다.')
    change=data['change']
    columns[1].metric('전분기 대비', ('비교 보류' if data.get('comparison_blocked') else '비교 자료 없음') if change is None else f'{change:+,}건',
                      delta=None if data['growth'] is None else f"{data['growth']:+.1f}%",
                      delta_color='off',delta_arrow='off',help='직전 분기와 비교합니다. 0건을 분모로 하는 증감률은 산출하지 않습니다.')
    claim=next((r for r in data['types'] if r['category'] in {'보상(보험금)','지급'}),None)
    share=None if claim is None or not data['total'] else claim['count']/data['total']*100
    columns[2].metric((claim['category'] if claim else '보상(보험금)')+' 유형',f"{claim['count']:,}건" if claim else '자료 없음',
                      delta=None if share is None else f'전체 민원의 {share:.1f}%',delta_color='off',delta_arrow='off',
                      help='보상 유형의 구성비입니다. 보험금 부지급률이나 소비자 피해율이 아닙니다.')
    columns[3].metric('보유계약 10만건당', '자료 없음' if data['rate'] is None else f"{data['rate']:.2f}",
                      help='공시 원문의 환산 민원건수. 분기말 회사 전체 보유계약 기준이며 원시 보유계약 수는 미확보입니다.')
