"""Collect public quarter tables; preserve baseline and verify every actual period."""
import hashlib
import json
from datetime import datetime,timezone
from urllib.parse import urlencode
from collections import Counter
from .client import Client, ROOT
from .expand_insurers import parse_knia, build_registry
from src.preprocessing.clean_stats import validate

TARGETS=['2024Q2','2024Q4','2025Q2','2025Q4']
BASE_URL='https://consumer.knia.or.kr/m/disclosure/item/01.do'


def previous(period):
    year,quarter=map(int,period.split('Q'))
    return f'{year}Q{quarter-1}' if quarter>1 else f'{year-1}Q4'


def key(row):
    return tuple(row[n] for n in ('company','period','axis','category'))


def normalized_rows(rows):
    aliases={'MG손보':'MG손해보험','캐롯손보':'캐롯손해보험','신한EZ손해보험':'신한EZ손해보험'}
    for row in rows:
        row['source_company_label']=row['company']
        row['company']=aliases.get(row['company'],row['company'])
        row['definition_regime']='협회 2024Q2 개선 이후' if row['period']>='2024Q2' else '협회 2024Q2 개선 이전'
        row['comparability_note']='2024년2분기 공시기준 개선 전후 직접 증감 비교 보류. 회사별 상세 분모·상품 구성 차이 유지.'
    return rows


def save(path,obj):
    target=ROOT/path
    target.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')


def main():
    baseline=ROOT/'data/processed/insurer_stats_all.json'
    before=hashlib.sha256(baseline.read_bytes()).hexdigest()
    originals=json.loads(baseline.read_text('utf-8'))
    combined=list(originals)
    known={key(r):r for r in originals}
    client=Client();sources=[];cross=[];excluded=[]
    for period in TARGETS:
        year,quarter=period.split('Q')
        url=BASE_URL+'?'+urlencode({'01_searchYear':year,'01_seasrchQuarter':quarter})
        path,receipt=client.fetch(url)
        source={'source_id':'knia_history_'+period.lower(),'source_page':url,'document':receipt}
        rows,_=parse_knia(path,source,[previous(period),period])
        rows=normalized_rows(rows)
        groups={ (r['company'],r['period']) for r in rows }
        bad_groups=set()
        for group in groups:
            selected=[r for r in rows if (r['company'],r['period'])==group]
            if any(not isinstance(r['count'],int) for r in selected):
                bad_groups.add(group)
                excluded.append({'company':group[0],'period':group[1],'reason':'원문 건수 결측: 0으로 채우지 않고 해당 항목 전체 보류'})
            else:
                group_checks=validate([],selected)
                failed=[c['check'] for c in group_checks if not c['passed']]
                if failed:
                    bad_groups.add(group)
                    totals={axis:sum(r['count'] for r in selected if r['axis']==axis and r['category']!='합계') for axis in ['접수경로','유형','상품']}
                    excluded.append({'company':group[0],'period':group[1],'reason':'원문 표의 분류축별 합계 불일치: 항목 전체 보류',
                        'axis_part_sums':totals,'failed_checks':failed,'source_url':url})
        rows=[r for r in rows if (r['company'],r['period']) not in bad_groups]
        checks=validate([],rows)
        if not all(c['passed'] for c in checks):
            raise ValueError(json.dumps([c for c in checks if not c['passed']],ensure_ascii=False))
        for row in rows:
            prior=known.get(key(row))
            if prior:
                cross.append({'key':list(key(row)),'passed':all(prior[f]==row[f] for f in ['count','rate_per_100k'])})
            else:
                known[key(row)]=row;combined.append(row)
        sources.append(source|{'expected_periods':[previous(period),period],'actual_companies':len({r['company'] for r in rows}),'observations':len(rows)})
        print(json.dumps({'source_period':period,'actual_periods':sorted({r['period'] for r in rows}),'companies':len({r['company'] for r in rows}),'rows':len(rows)},ensure_ascii=False),flush=True)
    if not all(c['passed'] for c in cross):raise ValueError('기존 공시와 과거 조회의 수치 충돌: 원본 유지, 저장 중단')
    checks=validate([],combined)
    if not all(c['passed'] for c in checks):raise ValueError('전체 과거 자료 검증 실패')
    if hashlib.sha256(baseline.read_bytes()).hexdigest()!=before:raise ValueError('기존 원본이 변경됨')
    registry=build_registry(combined)
    for company,entry in registry.items():
        group=[r for r in combined if r['company']==company]
        entry['periods']=sorted({r['period'] for r in group})
        entry['history_note']='2024Q2 공시기준 개선 전후의 비교와 회사명/계약 이관에 주의. 공시가 없는 회사·기간은 생성하지 않음.'
        if company in {'MG손해보험','예별손해보험'}:
            entry['history_note']+=' MG와 예별은 자동 병합하지 않으며 별도 항목으로 유지.'
        entry['caution']+=' '+entry['history_note']
        if company=='코리안리':
            entry['sector']='재보험'
            entry['caution']+=' 원문 회사 목록의 코리안리재보험입니다. 일반 원수보험사와 직접 비교하지 않습니다.'
    repeated=Client()
    for source in sources:repeated.fetch(source['source_page'])
    report={'generated_at':datetime.now(timezone.utc).isoformat(),'baseline_sha256':before,
        'baseline_unchanged':True,'baseline_observations':len(originals),'observations':len(combined),
        'added_observations':len(combined)-len(originals),'company_count':len(registry),
        'company_quarter_items':len({(r['company'],r['period']) for r in combined}),
        'period_counts':dict(sorted(Counter(r['period'] for r in combined if r['axis']=='접수경로' and r['category']=='합계').items())),
        'sources':sources,'checks':checks,'overlap_cross_checks':cross,'excluded':excluded,
        'http_calls':client.calls,'cache_repeat':{'hits':repeated.hits,'http_calls':repeated.calls},
        'definition_change_period':'2024Q2','rule':'협회 공식 안내에 따른 공시기준 개선. 이전/이후 자동 증감 비교 금지.',
        'company_identity_note':'원문 회사명을 보존. MG와 예별, 캐롯과 한화 등 회사/계약 이전은 자동 연결하지 않음.'}
    save('data/processed/insurer_stats_history.json',combined)
    save('data/metadata/insurer_registry_history.json',registry)
    save('data/metadata/insurer_history_sources.json',sources)
    save('reports/insurer_history.json',report)
    print(json.dumps({k:report[k] for k in ['company_count','company_quarter_items','observations','added_observations','period_counts','cache_repeat','excluded']},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
