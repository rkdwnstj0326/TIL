# =============================================================
# [심화] defaultdict - 없는 키를 자동으로 만들어주는 딕셔너리
# - 파이썬 내장 모듈 collections에서 제공 => import 필요
# - 문법: defaultdict(자료형)
#         defaultdict(int)  => 없는 키를 조회하면 0으로 자동 생성
#         defaultdict(list) => 없는 키를 조회하면 []로 자동 생성
# - 목적: '키가 있는지 먼저 확인하는' 반복 코드를 없애기
# =============================================================

# =============================================================
# [1] 기존 방식 - 매번 키 존재 여부를 확인해야 함
# - counts[char] += 1 을 바로 하면 첫 등장 글자에서 KeyError
#   => 그래서 if로 먼저 확인하고 0을 넣어주는 초기화가 필요
#
# =============================================================

# 기존: 기본 딕셔너리
text = 'banana'
counts = {}

for char in text:
    if char not in counts:  # 키가 있는지 매번 확인해야 함
        counts[char] = 0
    counts[char] += 1

print(counts)  # {'b': 1, 'a': 3, 'n': 2}


# =============================================================
# [2] defaultdict 활용 - 초기화 코드가 사라짐
# - defaultdict(int)에서 int는 함수 이름 (괄호 없이 전달)
#   int()를 호출하면 0이 나오므로, 기본값이 0이 되는 원리
# - 결과는 [1]번과 동일하지만 if문 3줄이 사라져 핵심 로직만 남음
# - 출력 형태는 defaultdict(<class 'int'>, {...}) 로 나옴
#   => 일반 딕셔너리처럼 보이게 하려면 dict()로 변환 (아래 참고)
# =============================================================

# 개선: defaultdict 활용
from collections import defaultdict

text = 'banana'
counts = defaultdict(int)  # 기본값을 정수(0)로 설정

for char in text:
    # 키 확인 불필요! 없으면 0으로 자동 생성 후 +1
    counts[char] += 1

print(counts)  # defaultdict(<class 'int'>, {'b': 1, 'a': 3, 'n': 2})


# =============================================================
# [3] 활용 - defaultdict(list)로 그룹핑하기
# - 없는 키를 조회하면 빈 리스트 []가 자동 생성됨
#   => 곧바로 .append()를 이어 쓸 수 있음
# - 일반 딕셔너리였다면 아래처럼 초기화가 먼저 필요했음
#     if color not in fruit_by_color:
#         fruit_by_color[color] = []
# - 개수 세기(int)와 그룹핑(list)이 defaultdict의 두 대표 용도
#
# 주의: 없는 키를 '조회만' 해도 키가 생성됨
#    print(fruit_by_color['blue']) 하면 []가 출력되면서
#    실제로 'blue' 키가 딕셔너리에 추가되어 버림
# =============================================================

# 활용 예제
# 색상별 과일 분류
fruits = [('red', 'apple'), ('yellow', 'banana'), ('red', 'cherry')]
fruit_by_color = defaultdict(list)

for color, fruit in fruits:
    # color 키가 없으면 빈 리스트 생성 -> append 바로 가능
    fruit_by_color[color].append(fruit)

print(
    fruit_by_color
)  # defaultdict(<class 'list'>, {'red': ['apple', 'cherry'], 'yellow': ['banana']})
print(
    dict(fruit_by_color)
)  # {'red': ['apple', 'cherry'], 'yellow': ['banana']}
