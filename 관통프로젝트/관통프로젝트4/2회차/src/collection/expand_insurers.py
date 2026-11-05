"""동일 분기 공식 공시 확장. 기존 65개 관측값을 수정하지 않고 별도 결과를 만든다."""
import hashlib
import json
import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from src.collection.client import Client, ROOT
from src.preprocessing.clean_stats import observations, validate
from src.preprocessing.hwp_text import extract_body

KNIA='https://consumer.knia.or.kr/m/disclosure/item/01.do'
KYOBO='https://www.kyobo.com/dgt/web/customer/customer-proposal/cval-prcn'
MANUAL='https://consumer.knia.or.kr/common/filedown.do?fileName=minwon'
PERIODS=['2026Q1','2026Q2']
ALIASES={'한화손보':'한화손해보험','롯데손보':'롯데손해보험','KB손보':'KB손해보험',
         'DB손보':'DB손해보험','하나손보':'하나손해보험','AXA손보':'AXA손해보험',
         'AIG손보':'AIG손해보험','농협손보':'NH농협손해보험',
         '라이나손보(에이스손보)':'라이나손해보험','서울보증':'서울보증보험'}


def read(name):
    return json.loads((ROOT/name).read_text('utf-8'))


def save(name, value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')


def require_periods(soup,periods=None):
    periods=periods or PERIODS
    text=re.sub(r'\s+','',soup.get_text(' ',strip=True))
    for role,period in [('당분기',periods[1]),('전분기',periods[0])]:
        year,quarter=period.split('Q')
        if not re.search(role+r'[:：]?'+year+r'년'+quarter+r'분기',text):
            raise ValueError('요청 분기와 실제 공시 본문의 대상기간이 일치하지 않습니다.')
    if not ('10만건' in text or '십만건' in text):
        raise ValueError('환산건수 단위 미확인')


def parse_knia(path,source,periods=None):
    periods=periods or PERIODS
    soup=BeautifulSoup(path.read_bytes(),'html.parser');require_periods(soup,periods)
    tables=soup.select('table')
    if len(tables)!=9:raise ValueError('협회 표 구조 변경')
    rows=[]
    # 모바일/PC 표가 한 문서에 함께 있으므로 각 축의 첫 본문 표만 읽는다.
    for index,axis in [(1,'접수경로'),(4,'유형'),(7,'상품')]:
        company=None
        for row_index,tr in enumerate(tables[index].select('tr'),1):
            cells=[c.get_text(' ',strip=True) for c in tr.find_all(['th','td'],recursive=False)]
            if len(cells)==9:
                company=ALIASES.get(cells[0],cells[0]);cells=cells[1:]
            if len(cells)!=8 or company is None:raise ValueError('협회 행/회사 식별 실패')
            pair=observations(company,axis,cells[0],cells[1:7],periods,source,None,' | '.join(cells))
            for row in pair:
                row.update(source_table=index,source_row_number=row_index,
                           source_column_role='당분기' if row['period']==periods[1] else '전분기',
                           retrieved_at=source['document']['retrieved_at'])
                if axis=='상품':
                    row['denominator_scope']='상품별/전체 구분 미확인: 협회 표에 상세 분모 문구 없음'
                    row['rate_unit']='보유계약 10만건당; 상품별 상세 분모 미확인'
            rows.extend(pair)
    if periods==PERIODS and len({r['company'] for r in rows})!=17:raise ValueError('협회 회사 목록 변경 확인 필요')
    company_sets=[{r['company'] for r in rows if r['axis']==axis} for axis in ['접수경로','유형','상품']]
    if not company_sets[0] or not all(s==company_sets[0] for s in company_sets):raise ValueError('협회 분류축의 회사 목록 불일치')
    return rows,soup


def parse_kyobo(path,source):
    soup=BeautifulSoup(path.read_bytes(),'html.parser');require_periods(soup)
    tables=soup.select('table');rows=[]
    def entries(table):
        result={}
        for tr in table.select('tr'):
            for sup in tr.select('sup'):sup.decompose()
            cells=[c.get_text(' ',strip=True) for c in tr.find_all(['th','td'],recursive=False)]
            if cells and cells[0] in {'유형','상품'}:cells=cells[1:]
            if len(cells)!=5:continue
            label=re.sub(r'\s+','',re.sub(r'주\d+\)','',cells[0]))
            if label in result:raise ValueError('교보 분류 중복')
            result[label]=(cells[1:4],' | '.join(cells))
        return result
    for i,axis in [(0,'접수경로'),(2,'유형'),(4,'상품')]:
        counts,rates=entries(tables[i]),entries(tables[i+1])
        if not counts or counts.keys()!=rates.keys():raise ValueError('건수/환산건수 분류 조인 실패')
        for label,(values,evidence) in counts.items():
            pair=observations('교보생명',axis,label,values+rates[label][0],PERIODS,source,None,
                              evidence+' || 환산: '+rates[label][1])
            for row in pair:
                row.update(source_table=[i,i+1],source_column_role='당분기' if row['period']==PERIODS[1] else '전분기',
                           retrieved_at=source['document']['retrieved_at'])
            rows.extend(pair)
    if len(rows)!=28:raise ValueError('교보 관측값 개수 변경')
    return rows


def build_registry(rows):
    registry={}
    for company in sorted({r['company'] for r in rows}):
        group=[r for r in rows if r['company']==company]
        life=company=='교보생명'
        caution=('생명보험 원문 분류(판매·유지·지급)를 유지합니다. 손해보험 유형과 일대일로 비교하지 않습니다. '
                 '금감원 즉시연금 전용코너 접수 민원을 총건수에서 제외한다는 별도 조건이 있습니다.' if life else
                 '동일한 손해보험 분류축입니다. 회사 규모·상품 구성·개별 제외조건을 보정한 순위가 아닙니다.')
        if company=='예별손해보험':caution+=' MG손해보험에서 이관된 계약에 대한 공시입니다.'
        product_confirmed=life or company in {'하나손해보험','신한EZ손해보험'}
        if not product_confirmed:caution+=' 협회 상품표의 상세 분모(상품별/전체)는 원문에서 확인되지 않아 상품 환산값 비교는 보류합니다.'
        registry[company]={
            'company':company,'sector':'생명보험' if life else '손해보험',
            'periods':sorted({r['period'] for r in group}),
            'source_url':next(r['source_url'] for r in group if r['period']==max(g['period'] for g in group)),
            'publisher':'교보생명' if life else ('기존 보험사 직접 공시' if company in {'하나손해보험','신한EZ손해보험'} else '손해보험협회 소비자포털'),
            'rate_unit':'분기말 보유계약 10만건당',
            'denominator':('접수경로·유형: 회사 전체 / 상품: 해당 상품별 보유계약' if product_confirmed else
                           '접수경로·유형: 회사 전체 / 상품: 상세 분모(상품별/전체) 미확인')+'. 원시 분모 수는 미확보',
            'categories':sorted({r['category'] for r in group if r['axis']=='유형' and r['category']!='합계'}),
            'definition_status':('비교 주의: 업권·제외조건 차이' if life else
                '분기·회사 전체 환산단위·분류축 확인 / 상품 분모 미확인' if not product_confirmed else
                '분기·환산단위·분류축 확인 / 완전 동등성 미보증'),
            'caution':caution}
    return registry


def main():
    client=Client();sources=[]
    for source_id,url in [('knia_2026q2',KNIA),('kyobo_2026q2',KYOBO)]:
        path,receipt=client.fetch(url)
        sources.append({'source_id':source_id,'source_page':url,'document':receipt})
    assoc,soup=parse_knia(ROOT/sources[0]['document']['local_path'],sources[0])
    life=parse_kyobo(ROOT/sources[1]['document']['local_path'],sources[1])
    manual_path,manual_receipt=client.fetch(MANUAL,'bin')
    manual_text=extract_body(manual_path)
    (ROOT/'data/private/knia_manual.txt').write_text(manual_text,encoding='utf-8')
    manual_terms=['2024.  6. 30.','중복','자율조정','합의취하','임의철회','B2B','소송관련',
                  '보험모집','보상(보험금)','장기보장성보험','자동차보험']
    manual_ok=all(term in manual_text for term in manual_terms)
    sources.append({'source_id':'knia_manual_20240630','source_page':MANUAL,'document':manual_receipt,'kind':'bin'})
    base_path=ROOT/'data/processed/insurer_stats.json'
    original_hash=hashlib.sha256(base_path.read_bytes()).hexdigest()
    base=read('data/processed/insurer_stats.json')
    key=lambda r:(r['company'],r['period'],r['axis'],r['category'])
    originals={key(r):r for r in base};cross=[];added=[]
    for row in assoc+life:
        if key(row) in originals:
            previous=originals[key(row)]
            cross.append({'check':'직접 공시↔협회 '+ ' / '.join(key(row)),
                          'passed':all(previous[v]==row[v] for v in ['count','rate_per_100k'])})
        else:added.append(row)
    combined=base+added
    checks=validate([],combined)+cross
    checks.append({'check':'협회 공식 작성 매뉴얼 공시대상·제외조건·분류 확인','passed':manual_ok})
    checks.append({'check':'기존 65개 관측값 원본 유지','passed':hashlib.sha256(base_path.read_bytes()).hexdigest()==original_hash and combined[:len(base)]==base})
    if not all(c['passed'] for c in checks):
        raise ValueError(json.dumps([c for c in checks if not c['passed']],ensure_ascii=False))
    # 저장 캐시를 다시 조회해서 해시·실제 파일 존재 및 HTTP 재호출 0회를 확인한다.
    repeat=Client()
    for source in sources:repeat.fetch(source['source_page'],source.get('kind','html'))
    registry=build_registry(combined)
    report={'generated_at':datetime.now(timezone.utc).isoformat(),'company_count':len(registry),
            'companies_by_sector':{s:sum(r['sector']==s for r in registry.values()) for s in ['손해보험','생명보험']},
            'common_period':'2026Q2','observations':len(combined),'original_observations':len(base),
            'original_sha256':original_hash,'added_observations':len(added),'checks':checks,
            'cross_source_count':len(cross),'sources':sources,
            'manual_review':{'date':'2024-06-30','body_extracted':True,
                'excluded':['중복·반복(자체 후 동일 대외민원 예외)','자율조정 성립','합의취하','임의철회','B2B','소송관련'],
                'product_denominator_explicit':False,
                'note':'협회 HTML 및 매뉴얼에 상품별 상세 분모 문구 없음. 새 15개사는 상품 환산값의 분모 구분을 미확인으로 저장'},
            'cache_repeat':{'hits':repeat.hits,'http_calls':repeat.calls},
            'not_included':[
                {'company':'NH농협생명','reason':'실제 최신 원문은 2026Q3/2026Q2. Q2/Q1 자료로 오인하지 않고 이번 동분기 확장에서 보류'},
                {'company':'KB손해보험 직접 홈페이지','reason':'실제 응답은 보안세션 오류 HTML. 협회가 독립 공개한 표로 수록'}],
            'policy_note':'협회 robots 경로는 JPEG 오류 이미지로 이동하여 유효한 정책 텍스트 없음. 정상 공개 HTML 1회만 저속 수집·영속 캐시. 허용 정책이나 재배포 허가로 해석하지 않음.',
            'limitations':['원시 보유계약 수는 미확보; 환산값에서 역산하지 않음',
                          '환산건수는 원문 값이며 상품별 합산 금지; 기타의 빈 값은 0이 아님',
                          '회사별 세부 제외조건의 완전 동등성은 미확정; 민원 품질/피해율 순위 아님',
                          '공개 사례는 업계 익명 사례이며 회사별 사건으로 배정하지 않음',
                          '공식 자료의 외부 재배포 조건은 별도 확인 필요']}
    save('data/metadata/insurer_sources.json',sources)
    save('data/metadata/insurer_registry.json',registry)
    save('data/processed/insurer_stats_all.json',combined)
    save('reports/insurer_expansion.json',report)
    print(json.dumps({k:report[k] for k in ['company_count','companies_by_sector','observations','added_observations','cross_source_count','cache_repeat']},ensure_ascii=False))


if __name__=='__main__':main()
