import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    A = list(map(int, input().split()))

    max_v = 0
    count = 0

    for k in range(N - 2):
        if A[k] == A[k + 2]:
            count += 1
            max_v = max(count, max_v)
        else:
            count = 0

    print(f'#{tc} {max_v + 2}')