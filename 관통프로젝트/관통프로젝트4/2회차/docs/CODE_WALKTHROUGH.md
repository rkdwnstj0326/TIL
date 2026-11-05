# FinVOC Korea — Python 초보자를 위한 코드 설명

1. `app.py`가 프로그램의 시작점입니다. JSON 데이터를 읽고 선택한 화면 함수를 부릅니다.
2. `src/ui/views.py`는 회사 선택과 공시 화면을, `src/ui/theme.css`는 색·여백·카드 모양을 정합니다.
3. `src/collection/client.py`는 자료를 가져옵니다. 이미 저장된 URL은 해시가 같은지 확인해 재사용합니다.
4. `src/preprocessing`은 PDF/HTML/HWP를 읽고 숫자와 문단을 Python dict/list로 정리합니다. 없는 값은 None으로 둡니다.
5. `src/analysis/dashboard.py`는 실제 행에서 합계와 전분기 대비 증감을 계산합니다. 다른 분류축의 건수는 더하지 않습니다.
6. `src/rag/data.py`는 한 회사·분기를 하나의 항목으로 만들고 검색할 텍스트를 구성합니다.
7. `src/rag/embedding.py`는 한국어 문장을 384개의 숫자로 표현합니다. 실제 학습된 ONNX 모델을 사용합니다. 토큰 제한128을 넘으면 문장을 창으로 나눠 끝부분까지 처리합니다.
8. `src/rag/store.py`는 이 숫자를 ChromaDB에 저장합니다. 회사 공시 메타데이터와 외부 본문은 별도 컬렉션이며, 검색할 때 선택 항목ID를 필터로 사용합니다.
9. `src/rag/pipeline.py`의 retrieve는 질문에서 검색어 추출 → 후보 선별 → 원문 수집/색인 → 의미 검색을 담당합니다. generate는 GMS에게 실제 근거로만 답하게 하고 인용 번호를 검사합니다. 이 둘을 LangGraph로 연결했습니다.
10. `src/rag/gms.py`는 이 프로젝트 .env의 키로만 GMS에 연결합니다. 키나 서버 응답 전문은 화면/로그에 출력하지 않습니다.
11. `src/ui/rag_view.py`는 항목별 대화를 나누고 결과와 실제 사용 출처를 표시합니다. 다른 회사·분기로 바꾸면 그 항목의 대화를 보여줍니다.
12. `scripts/build_submission.py`는 제출할 파일만 골라 ZIP을 만듭니다. 가상환경과 실제 .env를 제외합니다.

실제 수치·사례 → 검색된 근거 → 생성 답변 순서입니다. 모델이 항상 옳지는 않으므로 원문 확인과 답변 보류가 필요합니다.
실제 검사 과정에서 미래 기간 질문을 현재 수치로 바꿔 답한 오류가 발견됐고, 기간 검사로 차단했습니다.

디자인 수정: src/ui/theme.css. 화면 배치 수정: src/ui/views.py와 src/ui/rag_view.py.
검색 설정 변경: config/rag.json. 새 설정은 새 컬렉션을 사용하므로 메타데이터 색인을 준비해야 합니다.

[실제 RAG 설계](rag_design.md) · [테스트 결과](test_results.md)
