import sys
sys.stdin = open('input.txt')

T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    numbers = list(map(int, input().split()))

    total = 0

    for i in range(N):
        for j in range(N):
            if i == j:
                continue

            total += numbers[i] % numbers[j]

    print(f'#{tc} {total}')