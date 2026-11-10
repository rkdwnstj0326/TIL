import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    M = int(input())

    N = 0
    total = 0

    while total < M:
        N += 1
        total += N

    print(f'#{tc} {N}')