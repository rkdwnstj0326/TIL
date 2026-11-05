import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .client import Client,ROOT

def main():
    c=Client();records=[]
    for num in ['287509','279797']:
        page='https://eiec.kdi.re.kr/policy/materialView.do?num='+num
        path,record=c.fetch(page);soup=BeautifulSoup(path.read_bytes(),'html.parser')
        a=next(a for a in soup.select('a') if a.get_text(strip=True).lower().endswith('.pdf'))
        pdf_url=urljoin(page,a['href']);pdf,pdf_record=c.fetch(pdf_url,'pdf')
        records.append({'source_id':'kdi_'+num,'publisher':'금융감독원','official_mirror':'KDI 경제교육·정보센터',
                        'source_page':page,'filename_label':a.get_text(strip=True),'document':pdf_record})
    for source_id,url,kind in [
        ('hana_2026q1','https://www.hanainsure.co.kr/download/26ebb71969','pdf'),
        ('hana_disclosures','https://www.hanainsure.co.kr/w/consumer/finaneConsumer/complainDisclosures','html'),
        ('shinhanez_2026q2','https://www.shinhanez.co.kr/static/cpo/CPO600M0154.html','html'),
        ('fss_copyright','https://www.fss.or.kr/fss/main/contents.do?menuNo=200701','html'),
        ('fss_case_list','https://www.fss.or.kr/fss/job/fncCnflCase/list.do?menuNo=201195','html'),
        ('fss_decision_list','https://www.fss.or.kr/fss/bbs/B0000390/list.do?menuNo=201193','html')]:
        path,record=c.fetch(url,kind);records.append({'source_id':source_id,'source_page':url,'document':record})
    target=ROOT/'data/metadata/source_catalog.json'
    target.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'sources':len(records),'http_calls':c.calls,'cache_hits':c.hits}))
if __name__=='__main__':main()
