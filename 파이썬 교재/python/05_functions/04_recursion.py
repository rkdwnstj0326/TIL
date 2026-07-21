# =============================================================
# 재귀 함수 (Recursion)
# - 함수가 자기 자신을 다시 호출하는 방식
# - 반드시 '종료 조건(base case)'이 있어야 함
#   => 없으면 무한히 호출되다가 RecursionError 발생
#
# [동작 흐름] factorial(5)
#   5 * factorial(4)
#     4 * factorial(3)
#       3 * factorial(2)
#         2 * factorial(1)
#           1 * factorial(0) => 1  (종료 조건 도달)
#   => 되돌아오며 곱해져 최종 120
# =============================================================

def factorial(n):
    # 종료 조건: n이 0이면 1을 반환
    if n == 0:
        return 1
    else:
        # 재귀 호출: n과 n-1의 팩토리얼을 곱한 결과를 반환
        return n * factorial(n - 1)


# 팩토리얼 계산 예시
print(factorial(5))  # 120
