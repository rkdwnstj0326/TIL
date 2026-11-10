# 가장 먼저 생각해야하는 것
# 1부터 숫자를 하나씩 더하다가 합계가 M 이상이 되는 순간의 N을 구하는 것

# 필요한 변수 3개
# M : 목표 합계 / N : 현재 어디까지 더했는지 / total : 지금까지 더한 합계

import sys
sys.stdin = open('input.txt')

T = int(input())

for tc in range(1, T+ 1):
    M = int(input())

    N = 0 # 아직 1도 더하지 않은 상태
    total = 0 # 지금까지 더한 합계가 0이다

    while total < M:  # 합계가 5 이상이 되면 반복이 멈춰서 while문
        N = N + 1
        total = total + N

    print(f"#{tc} {N}")