################ 문자열 탐색 및 검증 ################
# =============================================================
# [탐색] find - 값의 위치를 반환하되, 없으면 -1
# - index와 하는 일은 같지만 '없을 때'의 반응이 다름
#   index: 에러 발생 / find: -1 반환
#   => 에러로 멈추면 곤란한 상황에서는 find가 더 안전
# =============================================================

# find
text = 'banana'
print(text.find('a'))  # 1
print(text.find('z'))  # -1

# =============================================================
# [검증] is~ 계열 - 조건에 맞는지 True/False로 답함
# - isupper : 모든 (알파벳) 글자가 대문자인가
# - islower : 모든 (알파벳) 글자가 소문자인가
#   => 'Hello'는 대문자도 소문자도 섞여 있어 둘 다 False
# =============================================================

# isupper
string1 = 'HELLO'
string2 = 'Hello'
print(string1.isupper())  # True
print(string2.isupper())  # False

# islower
print(string1.islower())  # False
print(string2.islower())  # False

# =============================================================
# isalpha - 문자열이 비어 있지 않고, 모든 글자가 '문자'인가
# - 여기서 '문자'는 영문 알파벳뿐 아니라 한글, 한자 등
#   유니코드상 문자로 분류되는 모든 글자를 포함
# - 숫자, 공백, 특수문자가 하나라도 섞이면 False
#   => '123heis98576ssh'는 숫자가 섞여 있어 False
# =============================================================

# isalpha
string1 = 'Hello'
string2 = '123heis98576ssh'
print(string1.isalpha())  # True
print(string2.isalpha())  # False


################ 문자열 조작 ################
# =============================================================
# [중요] 문자열은 불변(immutable)
# - 아래 메서드들은 원본을 바꾸지 않고 '새 문자열'을 만들어 반환
# - 그래서 결과를 쓰려면 반드시 변수에 다시 담아야 함
# =============================================================

# =============================================================
# replace - 특정 부분을 다른 문자열로 교체
# - 세 번째 인자로 '교체 횟수'를 제한할 수 있음 (앞에서부터)
#   => 1을 주면 처음 만난 'world' 하나만 교체
# =============================================================

# replace
text = 'Hello, world! world world'
new_text1 = text.replace('world', 'Python')
new_text2 = text.replace('world', 'Python', 1)
print(new_text1)  # Hello, Python! Python Python
print(new_text2)  # Hello, Python! world world

# =============================================================
# strip - 양쪽 '끝'의 특정 문자를 제거
# - 사용자 입력의 불필요한 공백을 정리할 때 자주 사용
# - 핵심: '양쪽 끝'만 처리, 문자열 '중간'은 건드리지 않음
# =============================================================

# strip
# 사용자 입력 등에서 불필요한 공백이 포함된 경우
text = '   Hello    World   '

# 1. 아무것도 지정하지 않으면 '공백(띄어쓰기, 탭, 엔터)'을 제거
clean_text = text.strip()

print(clean_text)
# 결과: 'Hello    World'
# (주의: 문자열 중간의 공백은 제거되지 않음)


# 2. 제거할 문자를 지정하는 경우
text = '!!!Hello World!!!'
print(text.strip('!'))
# 결과: 'Hello World'


# [심화] 문자열 집합으로 제거 (순서 상관 없음)
# - 인자로 준 문자들을 '한 덩어리'가 아니라 '문자 집합'으로 취급
# - 양쪽 끝에서 그 집합에 속한 문자가 나오는 동안 계속 제거
# 'w', '.', 'c', 'o', 'm' 중 하나라도 양쪽 끝에 있으면 계속 제거
url = 'www.example.com'
print(url.strip('w.com'))
# 결과: 'example'
# (왼쪽의 'www.'과 오른쪽의 '.com'이 모두 제거됨)


# =============================================================
# split - 문자열을 기준에 따라 잘라 '리스트'로 만듦
# - 인자 유무에 따라 동작이 미묘하게 다름 (아래 1번 vs 2번)
# =============================================================

# split
# 1. 공백을 기준으로 분리 (기본 동작)
# - 여러 개의 공백도 하나로 처리하며, 앞뒤 공백은 무시함
text = '  Hello    Python  '
print(text.split())
# 결과: ['Hello', 'Python']


# 2. 특정 문자를 기준으로 분리
# - 지정한 문자를 기준으로 '엄격하게' 분리함 (빈 문자열 발생 가능)
# - 기본 동작과 달리, 구분자가 연속되면 그 사이를 빈 문자열로 채움
data = '10,20,,30'
print(data.split(','))
# 결과: ['10', '20', '', '30']


# 3. 분할 횟수 제한 (maxsplit)
# - 앞에서부터 1번만 자르고 나머지는 그대로 둠
path = 'User/admin/documents'
print(path.split('/', maxsplit=1))
# 결과: ['User', 'admin/documents']


# =============================================================
# join - split의 반대: 리스트를 하나의 문자열로 합침
# - 문법 주의: '연결자'.join(리스트)  =>  연결자가 주인공
# - ' '.join(...) 은 각 요소 사이에 공백을 끼워 넣으라는 뜻
# =============================================================

# join
words = ['Python', 'is', 'awesome']

sentence1 = ' '.join(words)
sentence2 = '-'.join(words)

print(sentence1)  # Python is awesome
print(sentence2)  # Python-is-awesome


# =============================================================
# 대소문자 변환 계열 - 규칙만 조금씩 다름
# - capitalize : 맨 첫 글자만 대문자, 나머지는 소문자
# - title      : 각 단어의 첫 글자를 대문자
# - upper      : 전부 대문자
# - lower      : 전부 소문자
# - swapcase   : 대<->소문자를 서로 뒤집음
# =============================================================

# capitalize
text = 'heLLo, woRld!'
new_text1 = text.capitalize()
print(new_text1)  # Hello, world!

# title
new_text2 = text.title()
print(new_text2)  # Hello, World!

# upper
new_text3 = text.upper()
print(new_text3)  # HELLO, WORLD!

# lower
new_text4 = text.lower()
print(new_text4)  # hello, world!

# swapcase
new_text5 = text.swapcase()
print(new_text5)  # HEllO, WOrLD!
