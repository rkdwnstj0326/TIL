import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    A = list(map(int, input().split()))

    # 나머지의 합
    total = 0

    # 나눠지는 숫자 선택
    for i in range(N):
        # 나누는 숫자 선택
        for j in range(N):
            # if i != j:
            total += A[i] % A[j] 
            # i == j인 경우 나머지가 0이므로 if 생략 가능


    print(f'#{tc} {total}')

    