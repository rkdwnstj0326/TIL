# =============================================================
# [실습 1] 혈액형 인원수 세기
# - 리스트를 순회하며 각 혈액형이 몇 번 나오는지 딕셔너리로 집계
# - 같은 문제를 3가지 방법으로 풀어보며 코드가 어떻게 짧아지는지 비교
#
# =============================================================

# 각 혈액형의 인원수를 계산하는 딕셔너리를 생성하기.
blood_types = ['A', 'B', 'O', 'AB', 'A', 'O', 'B', 'A', 'AB', 'O', 'A', 'B']
"""
실행 결과
{'A': 4, 'B': 3, 'O': 3, 'AB': 2}
"""


# =============================================================
# [실습 포인트 1] [] 표기법 - 가장 기본적인 방법
# - 빈 딕셔너리를 만들고 리스트를 순회
# - 힌트: in 연산자로 키의 존재 여부를 확인할 수 있음
# =============================================================

# 1. [] 표기법을 사용한 방법
def count_blood_types_01(blood_types):
    # TODO: 결과를 담을 빈 딕셔너리를 만들고,
    #       리스트를 순회하며 개수를 세어 반환하세요
    result = {}
    for blood_type in blood_types:
        if blood_type in result:
            result[blood_type] = result[blood_type] + 1
        else:
            result[blood_type] = 1
    return result
# result = count_blood_types_01(blood_types)
# print(result)



# =============================================================
# [실습 포인트 2] get() 메서드 - if문 없이 처리하기
# - get(키, 기본값)은 키가 없을 때 기본값을 돌려줌
# - 힌트: 딕셔너리[혈액형] = 딕셔너리.get(혈액형, 0) + 1
# =============================================================

# 2. get() 메서드를 사용한 방법
def count_blood_types_02(blood_types):
    # TODO: get()의 기본값을 활용해 한 줄로 개수를 누적하세요
    result = {}
    for blood_type in blood_types:
        result[blood_type] = result.get(blood_type,0)+1

    return result

# print(count_blood_types_02(blood_types))


# =============================================================
# [실습 포인트 3] defaultdict - 초기화 자체를 없애기
# - defaultdict(int)는 없는 키를 조회하면 0을 자동 생성
# - 힌트: 반환할 때 dict()로 변환하면 일반 딕셔너리 형태로 출력됨
# =============================================================

# 3. defaultdict를 사용한 방법
from collections import defaultdict


def count_blood_types_03(blood_types):
    # TODO: defaultdict(int)를 사용해 가장 간결하게 작성하세요
    result = defaultdict(int)

    for blood_type in blood_types:
        result[blood_type] = result[blood_type] + 1

    return dict(result)



# -------------------------------------------------------------
# 테스트: 함수를 완성하기 전에는 pass 때문에 None이 출력됩니다
# -------------------------------------------------------------
print(count_blood_types_01(blood_types))  # {'A': 4, 'B': 3, 'O': 3, 'AB': 2}
print(count_blood_types_02(blood_types))  # {'A': 4, 'B': 3, 'O': 3, 'AB': 2}
print(count_blood_types_03(blood_types))  # {'A': 4, 'B': 3, 'O': 3, 'AB': 2}
