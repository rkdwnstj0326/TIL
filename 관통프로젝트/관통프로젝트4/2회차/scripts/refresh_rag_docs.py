"""Generate current documentation from actual validation files, not planned outcomes."""
import json
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]


def read(path, default=None):
    target = ROOT / path
    return json.loads(target.read_text('utf-8-sig')) if target.exists() else default


def write(path, text):
    (ROOT / path).write_text(text.strip() + '\n', encoding='utf-8')


def refresh():
    from src.rag.data import items,corpus
    catalog = items()
    data_rows,cases=corpus()
    hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in [
        'data/processed/insurer_stats_all.json','data/processed/insurer_stats_history.json',
        'data/processed/sector_stats.json','data/private/cases.json'] if (ROOT/name).exists()}
    write('reports/submission_profile.json',json.dumps({'theme':'FinVOC Korea','author':'서울_1반_강준서','as_of_date':'2026-10-23',
        'companies':len({r['company'] for r in data_rows}),'company_quarter_items':len(catalog),
        'company_observations':len(data_rows),'sector_observations':28,'public_case_documents':len(cases),
        'distinct_search_titles':len({c['title'] for c in cases}),'data_hashes':hashes},ensure_ascii=False,indent=2))
    live = read('reports/rag_comparison.json', {'questions': []})
    local = read('reports/rag_local_validation.json', {})
    connection = read('reports/gms_connection.json', {})
    suite = ET.parse(ROOT / 'reports/submission_pytest_20261023.xml').getroot().find('testsuite')
    tests = {'tests': int(suite.get('tests')), 'failures': int(suite.get('failures')), 'errors': int(suite.get('errors'))}
    rows = [
        ('F2001','항목 메타데이터 적재','구현·수량 검증',f'실제 회사·분기 {len(catalog)}개. 2024Q1~2026Q2. 같은 민원의 분류축을 별도 항목으로 세지 않음.','src/rag/data.py'),
        ('F2002','메타데이터 의미 색인','구현·로컬 검증','실제 다국어 MiniLM과 Chroma metadata 컬렉션.','src/rag/store.py'),
        ('F2003','검색어 추출 프롬프트','구현·실제 호출','한국어 검색어 JSON, 타입·범위 검사.','src/rag/prompts.py'),
        ('F2004','질문 시점 문서 수집·선별','구현·검색 범위 제한','기존 공식 목록 70개에서 검색·GMS 선별 후 원문 fetch. 웹 전체 최신 검색은 아님. 선택 공시 우선 수집.','src/rag/pipeline.py'),
        ('F2005','외부 문서 별도 색인','구현·로컬 검증','선별한 본문만 질문 시점에 별도 컬렉션에 색인.','src/rag/store.py'),
        ('F2006','근거 검색·병합','구현·로컬 검증','선택 메타데이터 상시 포함, item_id 필터, 실제 의미 검색/MMR.','src/rag/store.py'),
        ('F2007','근거 답변 생성','구현·대표 질문 실검증','LangGraph retrieve/generate 두 노드와 실제 GMS. 모델 기간 혼동을 발견해 검사로 보류.','src/rag/pipeline.py'),
        ('F2008','인용과 출처','구현·구조 검증','없는 인용/불일치 차단. 실제 인용된 제목·유형·본문·URL·수집일 표시. 전 문장 의미 검증은 아님.','src/ui/rag_view.py'),
        ('F2009','항목 선택·대화 분리','구현·일부 화면 검증','회사/분기별 session 대화. 위젯과 영속 선택값 분리로 메뉴 왕복 조건 유지.','src/ui/rag_view.py'),
        ('F2010','금융 특화 검토 지원','구현·제한적 검증','공시·업계 사례·검토 제안 구분, 익명 회사 귀속 금지, 분류축 합산 금지.','src/rag/prompts.py'),
        ('F2011','자연어 조건 탐색','구현·일부 검증','연도/분기/최소건수/업권 데이터 필터 + 의미 후보 검색 + 질문 항목 이동.','src/ui/rag_view.py'),
        ('F2012','진행·예외 안내','구현·일부 검증','키/색인/데이터/네트워크/JSON 오류 안내. AI 범위 밖과 근거 없는 기간 보류.','src/ui/rag_view.py'),
        ('F2013','프론트 분리','미선택','Streamlit/CSS 사용.','src/ui/theme.css'),
        ('F2014','MMR','구현·실제 비교','실제 ONNX/DB로 유사도/MMR 순서 차이 확인.','reports/rag_local_validation.json'),
        ('F2015','RAG 전후 비교','실제 실행·독립 평가 미완료','대표7문항 실제 응답과 이전 실패 기록. 개발자 선정 스모크이며 일반 정확도 아님.','reports/rag_comparison_summary.json'),
        ('F2016','다중 출처','일부 구현','공시와 금감원 사례 결합. 임의 출처 추가 없음.','src/rag/data.py'),
        ('NF2001','응답 시간','실측·기준 보장 아님','대표 질문별 실제 시간 기록. 최초 색인/호출 오류/재시도에 따라 변동.','reports/rag_comparison_summary.json'),
        ('NF2002','영속 캐시','구현·로컬 검증','검색어/선별 SQLite + 본문 SHA256 캐시 + DB 실제 존재 확인 후 완료 기록.','src/rag/pipeline.py'),
        ('NF2003','키 관리','구현·패키지 검사','현재 프로젝트 .env만 사용. Git·ZIP 제외.','src/rag/gms.py'),
        ('NF2004','내부 정보 비노출','구현·일부 검증','안전한 오류 메시지, 원문 HTML 이스케이프, 프롬프트/키/traceback UI 비노출.','src/rag/gms.py'),
        ('NF2005','모듈 분리','구현','collection/preprocessing/analysis/rag/ui/scripts/tests.','src/rag/pipeline.py'),
        ('NF2006','외부 API 예절','구현·캐시 검증','공식 허용 호스트·robots·간격·timeout·Retry-After. 기존 출처 캐시 사용, 최신 재수집 성공과 구분.','src/collection/client.py'),
        ('NF2007','출처·이용 조건','부분 확인','공식 출처·수집일 유지. 원문 재배포 허락 미확인으로 ZIP에서 원문/본문 제외.','docs/DATA_TERMS.md'),
    ]
    requirement_rows = [{'id': code,'title': title,'status': status,'current': description,'evidence': evidence,'kind': '심화' if code in ('F2013','F2014','F2015','F2016') else '필수' if code.startswith('F') else '비기능'} for code,title,status,description,evidence in rows]
    write('docs/submission_requirements.json', json.dumps({'requirements': requirement_rows}, ensure_ascii=False, indent=2))
    table = '\n'.join(f'|{r[0]}|{r[1]}|{r[2]}|{r[3]}|' for r in rows)
    write('docs/requirements.md', '# FinVOC Korea — 요구사항 정의서\n\n2026-10-23 · 서울 1반 강준서. 실제 구현·검사 기준.\n\n'
        '공식 공시와 익명 업계 사례를 분리해 금융소비자보호 담당자의 검토를 지원한다. 개별 사건의 지급/법률 결과를 확정하지 않는다.\n\n'
        '|번호|요구사항|상태|실제 범위|\n|---|---|---|---|\n'+table+f'\n\n회사·분기 항목 {len(catalog)}개로 약100개 수량 조건을 충족한다. 공식 셀프·상호 평가와 독립 품질 평가는 미반영이다.')
    write('docs/requirements_traceability.md', '# FinVOC Korea — 요구사항 대조표\n\n|번호|현재 상태|코드·증거|\n|---|---|---|\n' + '\n'.join(f'|{code}|{status}|[{evidence}](../{evidence})|' for code,_,status,_,evidence in rows))
    summary = {'actual_gms': live.get('actual_gms'), 'model': live.get('model'), 'actual_gms_calls': live.get('actual_gms_calls'),
        'human_accuracy_review_complete': False, 'questions': []}
    for record in live['questions']:
        safe = {k: v for k, v in record.items() if k not in ('used_sources', 'previous_attempts')}
        safe['used_sources'] = [{k:v for k,v in s.items() if k != 'text'} for s in record.get('used_sources', [])]
        safe['previous_attempt_count'] = len(record.get('previous_attempts', []))
        summary['questions'].append(safe)
    write('reports/rag_comparison_summary.json', json.dumps(summary, ensure_ascii=False, indent=2))
    qtable = '\n'.join(f'|{n}|{r["question"]}|{r.get("status", "실패")}|{r.get("status_matches_expected", False)}|{r.get("seconds", "미기록")}|'
                       for n, r in enumerate(summary['questions'], 1))
    write('docs/rag_comparison.md', '# FinVOC Korea — 실제 RAG 전후 비교\n\n실제 GMS 응답이며 모의 결과가 아니다. 개발자 선정 대표7문항 스모크 검사로 일반 정답률을 주장하지 않는다.\n\n'
        '|번호|질문|결과 상태|기대 상태 일치|실측 초(비교 호출 포함)|\n|---|---|---|---|---|\n'+qtable+
        '\n\n원문 없는 기본 답변과 RAG 답변은 [실제 비교 기록](../reports/rag_comparison_summary.json)에 있다. '
        '7번은 범위 밖 안내로 생성 호출을 생략했다. 일부 초기 호출 오류는 재시도했고 전체 로컬 기록에 보존했다. '
        '2030년 질문에 2026년 수치를 답한 오류를 발견했다. 기간 검사로 막았으며, 재실행에서도 모델 답변을 거부하고 시스템이 보류한 사실을 model_answer_rejected에 남겼다. '
        '인용 번호의 존재는 자동 검사했으나 모든 문장에 대한 독립 전문가 평가는 미완료다.')
    write('docs/test_results.md', f'# FinVOC Korea — 테스트 결과\n\n2026-10-23 기준.\n\n'
        f'- pytest: {tests["tests"]}개, 실패 {tests["failures"]}, 오류 {tests["errors"]}. 자동 시험의 GMS.json은 차단한다.\n'
        f'- 실제 GMS 연결: {connection.get("connected", False)}.\n'
        f'- 실제 ONNX/Chroma 검사: {sum(local.get("checks", {}).values())}/{len(local.get("checks", {}))}.\n'
        '- 임베딩 384차원, 실제 상한128토큰, 긴 한국어 전체 문자/끝 문장 보존, 재색인 중복/공유 문서 충돌/항목 필터/설정 변경/Top-k/MMR/반복 HTTP0회 검사.\n'
        '- 메뉴를 사례 탐색으로 이동한 뒤 돌아와도 삼성화재2026Q1 조건 유지 회귀 검사 추가.\n'
        '- 실제 GMS 대표7문항 실행. 모델의 기간 혼동은 검증기로 보류하고 이전 실패를 숨기지 않는다.\n'
        '- 원문 재수집 HTTP 검사가 아닌 기존 공식 캐시의 실제 본문 재사용 검사다. 최신성/일반 검색 정확도/실제 민원 감소 효과를 입증하지 않는다.\n\n'
        '- 실제 ZIP을 안전하게 풀고 데이터 없음 안내를 확인했다. 검증 폴더에 로컬 스냅샷5개만 복원한 뒤 화면과 키 없음 안내를 확인했다. 외부 HTTP/GMS는0회이며 새 컴퓨터 원격 수집 검사는 아니다.\n\n'
        '[로컬 검증](../reports/rag_local_validation.json) · [GMS 비교](../reports/rag_comparison_summary.json)')
    if (ROOT/'reports/insurer_history.json').exists():
        history=read('reports/insurer_history.json')
        text=(ROOT/'docs/test_results.md').read_text('utf-8')
        text+=f'\n\n## 과거 공시 확장 검증\n\n실제 {history["company_quarter_items"]}개 회사·분기 / {history["observations"]}개 관측값. '
        text+=f'부분합·축간합계·고유키·건수 검사 {len(history["checks"])}개 통과. 기존 겹침 {len(history["overlap_cross_checks"])}개 대조 통과. '
        text+='AIG 결측2분기·합계불일치1분기를 제외했고 기준 변경 전후의 증감과 누락 분기 연결을 차단했다. '
        text+='과거 원문 캐시4회 적중·HTTP0회. [과거 자료 상세](HISTORICAL_DATA.md).\n'
        text+='과거 GMS 대표2문항도 별도 실행했다. 접수건수와 환산값을 혼동한 초기 설명을 발견해 지침을 보완했고 이전 응답도 보존했다. '
        text+='[실제 기록](../reports/history_rag_validation.json)은 독립 전문가 정확도 평가가 아니다.\n'
        write('docs/test_results.md',text)
    status = {'project': 'FinVOC Korea', 'author': '서울_1반_강준서', 'as_of_date': '2026-10-23',
        'rag_implemented': True, 'actual_gms_connection_verified': connection.get('connected', False),
        'actual_rag_questions': len(live['questions']), 'automated_tests': tests, 'domain_item_count': len(catalog),
        'approx_100_item_requirement_satisfied': len(catalog) >= 100, 'mandatory_features_complete': False,
        'ready_for_final_submission': False, 'human_evaluations_received': False,
        'remaining': [],
        'uploaded': False}
    historical_live=read('reports/history_rag_validation.json',{'questions':[]})
    status['additional_historical_rag_questions']=len(historical_live['questions'])
    status['remaining'] = ([] if len(catalog)>=100 else [f'회사·분기 {len(catalog)}개로 약100개 조건 미충족'])+['공식 셀프·상호 평가 미반영', '독립 검색 정답셋·생성 답변 전문가 평가 미완료']
    write('SUBMISSION_STATUS.json', json.dumps(status, ensure_ascii=False, indent=2))
    write('docs/checklists.md', '# FinVOC Korea — 제출 전 점검\n\n이 문서는 공식 평가 결과가 아니다.\n\n'
        f'- 실제 GMS·벡터 RAG 구현과 검증 기록: 있음.\n- 회사·분기 {len(catalog)}개: 수량 조건 확인.\n'
        '- [테스트 결과](test_results.md)의 실제 검사 범위 확인.\n- 공식 셀프·받은 상호·보낸 상호 결과: 아직 미반영.\n'
        '- 실제 결과를 submission_human에 넣고 문서와 ZIP을 다시 생성할 것. 빈 보조 양식은 결과가 아니다.\n'
        '- 업로드 전 최종 ZIP의 가상환경·.env·키·DB·모델 캐시 제외 검사.\n- 업로드는 아직 진행하지 않음.')
    write('docs/submission_audit.md', '# FinVOC Korea — 제출 점검\n\n'
        '코드·문서·검증 결과는 2회차 안에 직접 관리한다. `제출용 압축.cmd`를 제출 직전에 실행한다.\n\n'
        '필수 제출 문서: README, 요구사항 정의/대조, RAG 설계, 테스트/화면 증거, 출처·이용조건, 공식 셀프·상호 결과.\n'
        '회사·분기 수량 조건은 충족했다. 공식 평가와 독립 품질 평가가 남아 최종 충족으로 표시하지 않는다.\n\n'
        'ZIP은 선생님 지정 파일명으로 dist 안에 생성한다. 실제 .env·가상환경·원문·정제 데이터·로컬 DB·모델 캐시는 제외한다. '
        '재현 시 README의 자료 준비 절차가 필요하며 원격 사이트 변경 시 실패할 수 있다.\n\n'
        '[제출 위치·파일명](SUBMISSION_INSTRUCTIONS_20261023.md) · [최신 상태](../SUBMISSION_STATUS.json)')
    return status


if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(ROOT))
    print(json.dumps(refresh(), ensure_ascii=False))
