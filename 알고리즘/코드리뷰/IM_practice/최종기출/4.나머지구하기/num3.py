import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    A = list(map(int, input().split()))

    total = 0

    for i in range(N):
        for j in range(N):
            total += A[i] % A[j]

    print(f'#{tc} {total}')