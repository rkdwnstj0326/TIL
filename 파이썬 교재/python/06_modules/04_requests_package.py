# =============================================================
# 패키지(Package) 사용 - 외부 라이브러리 활용
# - 모듈이 여러 개 모인 것이 패키지
# - math처럼 파이썬에 기본 포함된 것이 아니므로 '설치'가 필요함
#   설치 명령: pip install requests
# - requests : 파이썬에서 웹에 요청을 보내는 대표적인 패키지
#
# ⚠️ [실행 주의] 설치하지 않은 상태로 실행하면
#    ModuleNotFoundError: No module named 'requests' 발생
# =============================================================

# requests 패키지 사용 예제
# requests 패키지 설치해야 정상 동작

import requests
from pprint import pprint
# =============================================================
# [동작 흐름] 브라우저 주소창에 URL을 입력하는 것과 같은 일을 코드로 수행
#   1. requests.get(url)  : 해당 주소로 데이터를 요청
#   2. .json()            : 응답으로 받은 JSON 문자열을 딕셔너리/리스트로 변환
#   3. print(response)    : 변환된 파이썬 자료구조를 출력
# => 앞에서 배운 딕셔너리와 리스트가 실제 데이터로 등장하는 지점
# =============================================================

# 공휴일 정보 API
url = "https://date.nager.at/api/v3/publicholidays/2026/KR"
response = requests.get(url).json()
pprint(response)
