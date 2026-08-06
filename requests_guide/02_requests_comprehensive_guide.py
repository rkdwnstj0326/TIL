'''
==========================================================================
 requests 종합 가이드 - "요청을 보내고, 응답을 뜯어본다"
==========================================================================

 [이 파일의 목적]
   실습 노트북 Step 7 (API 와 HTTP) 의 TODO 를 풀기 전에,
   requests 가 "무엇을 돌려주는지" 를 눈으로 먼저 확인하기 위한 사전 참고 파일입니다.

 [사용 API]
   https://jsonplaceholder.typicode.com/users
   - 회원가입, API 키가 필요 없는 공개 연습용 API
   - 가짜 사용자 10명의 정보를 JSON 으로 돌려줍니다.

 [실행 방법] (가상환경에 requests가 설치되어 있다면 설치하지 않아도 됩니다.)
   $ pip install requests
   $ python 02_requests_comprehensive_guide.py

   STEP 이 하나 끝날 때마다 Enter 를 눌러 다음으로 넘어갑니다.
   (한 번에 쭉 보고 싶으면 아래 PAUSE 값을 False 로 바꾸세요)

 [핵심 한 줄]
   requests.get() 은 "데이터" 를 주는 게 아니라 "Response 객체" 를 줍니다.
   데이터는 그 객체 안에서 우리가 직접 꺼내야 합니다.
==========================================================================
'''

import json
import time

import requests

# --------------------------------------------------------------------------
# 실행 설정
# --------------------------------------------------------------------------
PAUSE = True  # True: STEP 마다 Enter 대기 / False: 한 번에 전체 실행

BASE_URL = 'https://jsonplaceholder.typicode.com/users'
POST_URL = 'https://jsonplaceholder.typicode.com/posts'


def title(step_no, text):
    '''STEP 제목을 보기 좋게 출력합니다. (학습 내용과 무관한 보조 함수)'''
    print()
    print('=' * 74)
    print(f' STEP {step_no}. {text}')
    print('=' * 74)


def pause():
    '''STEP 사이에서 잠시 멈춥니다. (학습 내용과 무관한 보조 함수)'''
    if not PAUSE:
        return
    try:
        input('\n  ... Enter 를 누르면 다음 STEP 으로 넘어갑니다 ...')
    except EOFError:
        # 파이프로 실행하는 등 입력이 없는 환경에서는 그냥 통과
        pass


# ==========================================================================
# STEP 1. 가장 짧은 요청 한 줄
# ==========================================================================
def step_01_first_request():
    '''
    [개념]
      브라우저 주소창에 URL 을 치는 행위 = 서버에게 GET 요청을 보내는 것.
      requests.get(url) 은 그 행위를 파이썬 코드로 대신하는 것입니다.

    [비유]
      requests.get(url)  =  식당에 전화를 걸어 "메뉴판 주세요" 라고 말하는 것
      response           =  택배로 도착한 "봉투"  (봉투 자체지, 내용물이 아님)

    [흐름]
      내 파이썬 코드 --(HTTP GET 요청)--> jsonplaceholder 서버
      내 파이썬 코드 <--(HTTP 응답)------ jsonplaceholder 서버
    '''
    title(1, '가장 짧은 요청 한 줄 - requests.get()')

    response = requests.get(BASE_URL, timeout=5)

    # 여기서 학생들이 가장 많이 하는 오해:
    #   "response 에 사용자 목록이 들어있겠지?" => 아닙니다.
    #   response 는 '봉투' 이고, 사용자 목록은 봉투 '안' 에 있습니다.
    print('  response 를 그냥 출력하면:', response)
    print('  response 의 타입      :', type(response))

    print()
    print('  [정리] requests.get() 의 반환값은 데이터가 아니라 Response 객체입니다.')
    print('         그래서 다음 STEP 에서 이 봉투를 하나씩 열어봅니다.')


# ==========================================================================
# STEP 2. 봉투 뜯어보기 - Response 객체의 속성들
# ==========================================================================
def step_02_inspect_response():
    '''
    [개념]
      Response 객체에는 '내용물' 뿐 아니라 '배송 정보' 도 함께 들어 있습니다.
      요청이 잘 갔는지, 얼마나 걸렸는지, 실제로 어떤 주소로 갔는지 등.

    [자주 쓰는 속성]
      .status_code : 처리 결과 숫자 (200 성공, 404 없음, 500 서버 오류)
      .ok          : status_code 가 400 미만이면 True
      .url         : 실제로 요청이 나간 최종 URL
      .elapsed     : 요청부터 응답까지 걸린 시간
      .headers     : 응답 헤더 (내용물의 '포장 라벨')
      .encoding    : 본문 해석에 사용한 문자 인코딩
    '''
    title(2, '봉투 뜯어보기 - Response 객체의 속성')

    response = requests.get(BASE_URL, timeout=5)

    print('  .status_code :', response.status_code)  # 200 이면 성공
    print('  .ok          :', response.ok)  # 200번대면 True
    print('  .url         :', response.url)  # 실제 요청 주소
    print('  .elapsed     :', response.elapsed.total_seconds(), '초')
    print('  .encoding    :', response.encoding)

    print()
    print('  .headers 중 우리가 확인할 것:')
    # 헤더는 dict 처럼 생겼습니다. 대소문자를 구분하지 않고 접근할 수 있습니다.
    print('    Content-Type   :', response.headers.get('Content-Type'))
    print('    Content-Length :', response.headers.get('Content-Length'))

    print()
    print('  [실무 팁] Content-Type 에 application/json 이 있는지 먼저 확인하세요.')
    print('           HTML 을 돌려주는 서버에 .json() 을 부르면 그대로 터집니다.')


# ==========================================================================
# STEP 3. (가장 중요) .text 와 .json() 의 차이
# ==========================================================================
def step_03_text_vs_json():
    '''
    [개념]
      서버가 보내주는 응답 본문은 '언제나' 글자(문자열) 입니다.
      JSON 은 데이터 형식이 아니라 '글자로 데이터를 표현하는 약속' 입니다.

      .text   : 받은 그대로의 문자열 (str)
      .json() : 그 문자열을 파이썬 자료형(list / dict) 으로 '번역' 한 결과

    [비유]
      .text   = 외국어로 적힌 편지 원문
      .json() = 그 편지를 한국어로 번역한 결과 (이제 내용을 다룰 수 있음)

    [학생들이 100% 만나는 에러]
      response.text[0]['name']  =>  TypeError
      문자열을 자른 것이지 dict 가 아니기 때문입니다.
    '''
    title(3, '.text 와 .json() 의 차이 (오늘의 핵심)')

    response = requests.get(BASE_URL, timeout=5)

    text_data = response.text  # 문자열
    json_data = response.json()  # 파이썬 객체 (여기서는 list)

    print('  .text 의 타입   :', type(text_data))
    print('  .json() 의 타입 :', type(json_data))

    print()
    print('  .text 앞 80글자 (그냥 글자입니다):')
    print('   ', text_data[:80], '...')

    print()
    print('  .json() 은 파이썬 자료형이므로 인덱싱과 키 접근이 됩니다:')
    print('    json_data[0]["name"]  =>', json_data[0]['name'])

    print()
    print('  문자열에 키로 접근하면 어떻게 되는지 직접 확인해 봅니다:')
    try:
        text_data[0]['name']  # 일부러 틀린 코드
    except TypeError as e:
        print('    TypeError 발생 =>', e)

    print()
    print('  [정리] 서버에서 받은 건 항상 글자. 다루려면 .json() 으로 번역할 것.')


# ==========================================================================
# STEP 4. 받은 데이터의 구조를 파악하는 순서
# ==========================================================================
def step_04_explore_structure():
    '''
    [개념]
      처음 보는 API 응답은 절대 '추측' 하지 않습니다. 아래 3단계로 확인합니다.
        1) type()  - 리스트인가 딕셔너리인가
        2) len()   - 몇 개인가
        3) keys()  - 어떤 키가 있는가

    [데이터 흐름 시각화]
      data (list)
        └─ data[0] (dict)
             ├─ 'name'    : 'Leanne Graham'
             ├─ 'email'   : 'Sincere@april.biz'
             ├─ 'address' (dict)
             │     └─ 'city' : 'Gwenborough'
             └─ 'company' (dict)
                   └─ 'name' : 'Romaguera-Crona'
    '''
    title(4, '받은 데이터의 구조 파악하기 (type -> len -> keys)')

    data = requests.get(BASE_URL, timeout=5).json()

    # 1) 바깥이 무엇인가
    print('  1) type(data) :', type(data))
    # 2) 몇 개인가
    print('  2) len(data)  :', len(data))
    # 3) 한 칸 안에는 어떤 키가 있는가
    first = data[0]
    print('  3) 첫 사용자의 키 :', list(first.keys()))

    print()
    print('  중첩된 dict 안까지 들어가 봅니다:')
    print('    address 의 키 :', list(first['address'].keys()))
    print('    company 의 키 :', list(first['company'].keys()))

    print()
    print('  중첩 접근은 바깥에서 안쪽으로 순서대로:')
    print('    data[0]["address"]["city"] =>', data[0]['address']['city'])

    print()
    print('  구조 전체를 보고 싶을 때는 json.dumps 로 예쁘게 출력합니다:')
    # ensure_ascii=False 를 빼면 한글이 \uXXXX 로 깨져 보입니다.
    print(json.dumps(first, indent=2, ensure_ascii=False)[:300], '...')


# ==========================================================================
# STEP 5. 조건을 붙여 요청하기 - params
# ==========================================================================
def step_05_query_params():
    '''
    [개념]
      GET 요청은 본문이 없습니다. 조건은 URL 뒤 '쿼리 스트링' 에 싣습니다.
        .../users?id=1&_limit=2

      requests 는 params 에 dict 를 넘기면 이 문자열을 대신 만들어 줍니다.

    [왜 문자열을 직접 이어붙이면 안 되는가]
      공백, 한글, & 같은 특수문자는 URL 에 그대로 넣을 수 없습니다.
      params 를 쓰면 requests 가 알아서 퍼센트 인코딩을 해 줍니다.
    '''
    title(5, '조건 붙여 요청하기 - params (문자열 이어붙이기 금지)')

    # 방법 A. 나쁜 예 - 직접 이어붙이기 (특수문자에서 반드시 사고가 납니다)
    bad_url = BASE_URL + '?id=1'
    print('  [나쁜 예] 직접 조립한 URL :', bad_url)

    # 방법 B. 권장 - params 에 dict 를 넘긴다
    response = requests.get(BASE_URL, params={'id': 1}, timeout=5)
    print('  [권장]   params 로 만든 URL :', response.url)
    print('  결과 개수 :', len(response.json()))

    print()
    print('  값이 여러 개인 조건도 dict 로 표현됩니다:')
    response = requests.get(BASE_URL, params={'id': 1, '_limit': 2}, timeout=5)
    print('    최종 URL :', response.url)

    print()
    print('  공백과 한글이 어떻게 자동 인코딩되는지 확인해 봅니다:')
    response = requests.get(BASE_URL, params={'q': '김싸피 테스트'}, timeout=5)
    print('    최종 URL :', response.url)
    print('    => 한글과 공백이 %XX 형태로 안전하게 변환되었습니다.')


# ==========================================================================
# STEP 6. 실패한 요청도 '성공적으로' 돌아온다 - status_code
# ==========================================================================
def step_06_status_code():
    '''
    [개념 - 가장 헷갈리는 지점]
      404 응답을 받아도 requests 는 예외를 던지지 않습니다.
      "서버가 '없다' 고 정상적으로 대답했다" 는 뜻이기 때문입니다.

      즉, 통신 성공 != 요청 성공. 이 둘은 반드시 구분해야 합니다.

    [상태 코드 첫 자리로 구분]
      2xx : 성공          (200 OK, 201 Created)
      4xx : 요청한 쪽 잘못 (404 없음, 401 인증 실패, 429 요청 과다)
      5xx : 서버 쪽 잘못   (500 내부 오류, 503 점검 중)

    [raise_for_status()]
      4xx / 5xx 이면 HTTPError 예외를 대신 발생시켜 주는 편의 메서드입니다.
      if 문을 매번 쓰는 대신 try/except 로 흐름을 모을 수 있습니다.
    '''
    title(6, '실패한 요청도 예외 없이 돌아온다 - status_code / raise_for_status')

    # 존재하지 않는 사용자 999번을 일부러 요청합니다.
    missing_url = f'{BASE_URL}/999'
    response = requests.get(missing_url, timeout=5)

    print('  요청 주소    :', missing_url)
    print('  status_code :', response.status_code)  # 404
    print('  .ok         :', response.ok)  # False
    print('  => 예외가 발생하지 않았습니다. 코드가 그냥 다음 줄로 흘러갑니다.')

    print()
    print('  raise_for_status() 를 부르면 그제서야 예외가 발생합니다:')
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('    HTTPError 발생 =>', e)

    print()
    print('  정상 요청(200)에서는 raise_for_status() 가 아무 일도 하지 않습니다:')
    ok_response = requests.get(f'{BASE_URL}/1', timeout=5)
    ok_response.raise_for_status()  # 조용히 통과
    print('    status_code :', ok_response.status_code, '/ 통과')
    print('    사용자 이름 :', ok_response.json()['name'])


# ==========================================================================
# STEP 7. timeout 과 예외 처리
# ==========================================================================
def step_07_timeout_and_exceptions():
    '''
    [개념]
      네트워크는 '항상 실패할 수 있는' 작업입니다.
      timeout 을 주지 않으면 서버가 응답하지 않을 때 프로그램이 무한정 멈춥니다.

    [반드시 구분해야 할 4가지 예외]
      Timeout          : 시간 안에 응답이 오지 않음        => 재시도 대상
      ConnectionError  : 서버에 아예 연결하지 못함(DNS 등)  => 주소/네트워크 확인
      HTTPError        : raise_for_status() 가 4xx/5xx 감지 => 요청 내용 확인
      JSONDecodeError  : 본문이 JSON 이 아님               => 응답 형식 확인

    [실무 팁]
      except Exception 하나로 뭉뚱그리면 원인을 영원히 알 수 없습니다.
      원인별로 나눠야 '재시도할지 / 코드를 고칠지' 판단할 수 있습니다.
    '''
    title(7, 'timeout 과 예외 처리 - 네트워크는 항상 실패할 수 있다')

    print('  timeout=0.001 초로 일부러 시간을 부족하게 만들어 봅니다:')
    try:
        requests.get(BASE_URL, timeout=0.001)
    except requests.exceptions.Timeout:
        print('    Timeout 발생 => 지정한 시간 안에 응답이 오지 않았습니다.')
    except requests.exceptions.ConnectionError:
        print('    ConnectionError 발생 => 서버에 연결하지 못했습니다.')

    print()
    print('  존재하지 않는 도메인으로 요청해 봅니다:')
    try:
        requests.get('https://no-such-domain-ssafy-15.com', timeout=3)
    except requests.exceptions.ConnectionError:
        print('    ConnectionError 발생 => 주소 자체를 찾지 못했습니다.')

    print()
    print('  JSON 이 아닌 응답에 .json() 을 부르면:')
    try:
        html_response = requests.get('https://example.com', timeout=5)
        html_response.json()
    except json.JSONDecodeError:
        print('    JSONDecodeError 발생 => 본문이 JSON 형식이 아닙니다.')
    except requests.exceptions.RequestException as e:
        print('    요청 자체 실패 =>', type(e).__name__)

    print()
    print('  [정리] RequestException 은 requests 예외들의 부모입니다.')
    print('         구체적인 예외를 먼저 쓰고, 맨 아래에 RequestException 을 둡니다.')


# ==========================================================================
# STEP 8. 헤더 붙이기 - headers
# ==========================================================================
def step_08_headers():
    '''
    [개념]
      헤더는 요청에 붙이는 '메모지' 입니다. 본문(데이터)이 아니라 부가 정보입니다.
        User-Agent    : 누가 요청했는가
        Accept        : 어떤 형식으로 받고 싶은가
        Authorization : 인증 토큰 (실무 API 대부분이 요구)

    [보안 주의]
      Authorization 에 들어갈 실제 키는 코드에 직접 쓰지 않습니다.
      환경변수나 .env 파일로 분리하고, .gitignore 에 반드시 등록합니다.
    '''
    title(8, '헤더 붙이기 - headers (인증의 출발점)')

    headers = {
        'User-Agent': 'SSAFY-15th-Python-Class',
        'Accept': 'application/json',
        # 'Authorization': 'Bearer <절대 코드에 직접 쓰지 않습니다>',
    }
    response = requests.get(BASE_URL, headers=headers, timeout=5)

    print('  status_code :', response.status_code)
    print()
    print('  내가 실제로 보낸 요청 헤더는 .request.headers 로 확인합니다:')
    for key in ('User-Agent', 'Accept'):
        print(f'    {key:<12}:', response.request.headers.get(key))

    print()
    print('  [디버깅 팁] 요청이 이상할 때 response.request 를 보면')
    print('             "내가 실제로 무엇을 보냈는지" 를 확인할 수 있습니다.')


# ==========================================================================
# STEP 9. 데이터를 보내는 요청 - POST (data= 와 json= 의 차이)
# ==========================================================================
def step_09_post_request():
    '''
    [개념]
      GET  : 가져오기. 조건은 URL 에.
      POST : 보내기.   데이터는 '본문(body)' 에.

    [data= 와 json= 의 결정적 차이]
      data=payload  => Content-Type: application/x-www-form-urlencoded (HTML 폼 형식)
      json=payload  => Content-Type: application/json  + 자동 직렬화

      요즘 API 는 대부분 JSON 을 요구하므로 json= 을 씁니다.
      LLM API(OpenAI, Anthropic 등) 호출도 전부 이 json= 방식입니다.

    [참고]
      jsonplaceholder 는 연습용이라 실제로 저장하지는 않고,
      "저장한 척" 하며 201 Created 와 함께 보낸 데이터를 돌려줍니다.
    '''
    title(9, '데이터를 보내는 요청 - POST (data= vs json=)')

    payload = {
        'title': 'requests 첫걸음',
        'body': '오늘 배운 내용 정리',
        'userId': 1,
    }

    print('  [A] json=payload 로 보내기 (권장)')
    response = requests.post(POST_URL, json=payload, timeout=5)
    print('    status_code  :', response.status_code)  # 201 Created
    print('    보낸 Content-Type :', response.request.headers.get('Content-Type'))
    print('    서버 응답    :', response.json())

    print()
    print('  [B] data=payload 로 보내면 형식이 달라집니다')
    response = requests.post(POST_URL, data=payload, timeout=5)
    print('    보낸 Content-Type :', response.request.headers.get('Content-Type'))
    print('    보낸 본문         :', response.request.body)

    print()
    print('  [정리] 서버가 JSON 을 기대하는데 data= 로 보내면')
    print('         400 Bad Request 가 나옵니다. 실무에서 가장 흔한 실수 중 하나입니다.')


# ==========================================================================
# STEP 10. 여러 번 요청할 때 - Session
# ==========================================================================
def step_10_session():
    '''
    [개념]
      requests.get() 을 부를 때마다 매번 새로 연결을 맺습니다.
      Session 을 쓰면 연결을 재사용하고, 공통 헤더도 한 번만 설정합니다.

    [비유]
      requests.get()  = 요청할 때마다 매번 전화를 새로 거는 것
      Session         = 통화를 연결해 두고 여러 건을 이어서 물어보는 것

    [실무 팁]
      반복 호출이 3회 이상이면 Session 을 쓰는 습관을 들이세요.
      with 문을 쓰면 끝날 때 자동으로 정리됩니다.
    '''
    title(10, '여러 번 요청할 때 - Session 으로 연결 재사용')

    target_ids = [1, 2, 3]

    # 방법 A. 매번 새 연결
    start = time.perf_counter()
    for user_id in target_ids:
        requests.get(f'{BASE_URL}/{user_id}', timeout=5)
    elapsed_plain = time.perf_counter() - start

    # 방법 B. Session 재사용
    start = time.perf_counter()
    with requests.Session() as session:
        # 공통 헤더는 한 번만 설정하면 이후 모든 요청에 자동 적용됩니다.
        session.headers.update({'Accept': 'application/json'})
        for user_id in target_ids:
            session.get(f'{BASE_URL}/{user_id}', timeout=5)
    elapsed_session = time.perf_counter() - start

    print(f'  개별 요청 3회 : {elapsed_plain:.3f} 초')
    print(f'  Session 3회   : {elapsed_session:.3f} 초')
    print()
    print('  네트워크 상황에 따라 차이는 달라지지만, 호출 수가 많을수록 격차가 커집니다.')


# ==========================================================================
# STEP 11. 지금까지 배운 것을 함수 하나로 - 실무 패턴
# ==========================================================================
def fetch_users(url=BASE_URL, timeout=5):
    '''
    지금까지의 STEP 을 실무에서 쓰는 형태로 합친 함수입니다.

    [설계 원칙]
      1) timeout 은 반드시 지정한다.
      2) raise_for_status() 로 4xx/5xx 를 걸러낸다.
      3) 예외는 원인별로 구분해 처리한다.
      4) 실패 시 무엇을 돌려줄지(빈 리스트) 미리 정한다.

    Returns:
        list: 사용자 dict 의 리스트. 실패하면 빈 리스트.
    '''
    try:
        response = requests.get(url, timeout=timeout)  # 1) 요청
        response.raise_for_status()  # 2) 상태 코드 검증
        return response.json()  # 3) 파이썬 객체로 변환
    except requests.exceptions.Timeout:
        print('  [실패] 응답 시간 초과. 잠시 후 재시도하세요.')
    except requests.exceptions.ConnectionError:
        print('  [실패] 서버에 연결할 수 없습니다. 네트워크와 주소를 확인하세요.')
    except requests.exceptions.HTTPError as e:
        print(f'  [실패] HTTP 오류: {e}')
    except json.JSONDecodeError:
        print('  [실패] 응답이 JSON 형식이 아닙니다.')
    return []


def step_11_practical_pattern():
    '''STEP 1~10 을 하나의 재사용 가능한 함수로 묶어 사용합니다.'''
    title(11, '실무 패턴 - 안전한 요청 함수로 묶기')

    users = fetch_users()

    if not users:
        print('  데이터를 가져오지 못했습니다. 위 실패 메시지를 확인하세요.')
        return

    print(f'  총 {len(users)}명을 가져왔습니다. 앞 3명만 정리해 봅니다:')
    print()
    print(f'  {"이름":<20}{"도시":<16}{"회사"}')
    print('  ' + '-' * 60)
    for user in users[:3]:
        name = user['name']
        # address 와 company 는 반드시 있는 키이므로 [] 로 접근
        city = user['address']['city']
        # website 처럼 없을 수도 있는 키는 .get() 으로 접근
        company = user['company']['name']
        print(f'  {name:<20}{city:<16}{company}')

    print()
    print('  [연결 고리] 이 users 리스트가 노트북 Step 8 의 data 와 같은 값입니다.')
    print('             이제 TODO 11~13 을 풀 준비가 끝났습니다.')


# ==========================================================================
# 실행부
# ==========================================================================
def check_network():
    '''시작 전에 API 에 실제로 연결되는지 한 번 확인합니다.'''
    try:
        response = requests.get(BASE_URL, timeout=5)
        response.raise_for_status()
        response.json()
        print('#  네트워크 점검: 정상 (API 응답 확인)')
        return True
    except Exception as e:
        print(f'#  네트워크 점검: 실패 ({type(e).__name__})')
        print('#  => 교육장 방화벽/프록시 문제일 수 있습니다.')
        print('#     연결이 필요한 STEP 은 자동으로 건너뛰고 진행합니다.')
        return False


def main():
    print()
    print('#' * 74)
    print('#  requests 첫걸음 가이드 - 요청을 보내고 응답을 뜯어봅니다')
    print(f'#  requests 버전: {requests.__version__}')
    print(f'#  대상 API: {BASE_URL}')
    check_network()
    print('#' * 74)

    steps = [
        step_01_first_request,
        step_02_inspect_response,
        step_03_text_vs_json,
        step_04_explore_structure,
        step_05_query_params,
        step_06_status_code,
        step_07_timeout_and_exceptions,
        step_08_headers,
        step_09_post_request,
        step_10_session,
        step_11_practical_pattern,
    ]

    for step in steps:
        try:
            step()
        except (
            requests.exceptions.RequestException,
            json.JSONDecodeError,
            KeyError,
            IndexError,
        ) as e:
            # 교육장 네트워크가 막혀 있어도 가이드 전체가 중단되지 않도록 처리
            print(f'\n  [이 STEP 을 건너뜁니다] {type(e).__name__}: {e}')
        pause()

    print()
    print('=' * 74)
    print(' 정리: 오늘 반드시 가져가야 할 4가지')
    print('=' * 74)
    print('  1. requests.get() 은 데이터가 아니라 Response 객체를 돌려준다.')
    print('  2. .text 는 글자, .json() 은 파이썬 자료형. 다루려면 .json().')
    print('  3. 404 도 예외 없이 돌아온다. raise_for_status() 로 걸러낸다.')
    print('  4. timeout 없는 요청은 언젠가 프로그램을 멈춘다.')
    print()
    print(' 다음 단계: 실습 노트북 Step 7 의 TODO 11 을 풀어 보세요.')
    print()


if __name__ == '__main__':
    main()
