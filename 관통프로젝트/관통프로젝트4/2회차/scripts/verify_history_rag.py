"""Explicit real GMS smoke check for newly collected historical metadata."""
import argparse,json,sys,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.rag.config import settings
from src.rag.data import items,corpus
from src.rag.embedding import LocalEmbedding
from src.rag.store import Store
from src.rag.gms import GMS
from src.rag.pipeline import Pipeline


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run',action='store_true')
    args=parser.parse_args()
    if not args.run:
        print('미실행: --run은 실제 GMS 사용량을 소모합니다.');return
    cfg=settings();catalog=items();store=Store(cfg,LocalEmbedding(cfg));store.index_items(catalog)
    client=GMS(cfg);pipe=Pipeline(cfg,store,corpus()[1],client)
    result=[]
    for company,period,question in [
        ('삼성화재','2025Q4','2025년4분기 민원 접수 합계와 당시 공시 수치 해석의 주의사항을 알려줘.'),
        ('하나손해보험','2024Q2','2024년2분기의 전분기 대비 민원 증감으로 개선됐다고 해석해도 돼?')]:
        item=next(i for i in catalog if i['company']==company and i['period']==period)
        start=time.perf_counter();state=pipe.run(item,question);answer=state['result']
        result.append({'company':company,'period':period,'question':question,'answer':answer['answer'],
            'status':answer['status'],'mode':answer['mode'],'expected_total':item['total'],
            'total_present':str(item['total']) in answer['answer'].replace(',','') if period=='2025Q4' else None,
            'correct_item_filter':all(s['item_id']==item['item_id'] for s in state['sources']),
            'citations_valid':all(1<=n<=len(state['sources']) for n in answer['cited_numbers']),
            'definition_boundary_abstained':answer['status']=='확인 불가' if period=='2024Q2' else None,
            'model_answer_rejected':answer.get('model_answer_rejected',False),'seconds':round(time.perf_counter()-start,3),
            'source_urls':sorted({s['url'] for s in answer['used_sources']})})
    report={'generated_at':datetime.now(timezone.utc).isoformat(),'actual_gms':True,'gms_calls':client.calls,
        'questions':result,'scope':'대표2문항 스모크. 독립 정확도/법률 판단 검증 아님.'}
    target=ROOT/'reports/history_rag_validation.json'
    if target.exists():
        prior=json.loads(target.read_text('utf-8'))
        report['previous_attempts']=prior.get('previous_attempts',[])+[{k:v for k,v in prior.items() if k!='previous_attempts'}]
        report['correction_note']='이전 답변에 접수 건수와10만계약당 환산값의 단위 혼동, 비교 보류와0변화 혼동 표현을 확인해 프롬프트를 보완했다. 전 문장 독립 전문가 검증은 미완료.'
    (ROOT/'reports/history_rag_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
