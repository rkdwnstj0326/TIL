import sys
sys.stdin = open('input.txt')

T = 10
for tc in range(1, T + 1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(100)]

    max_total = 0

    # 각 행의 합
    for r in range(100):
        total = 0
        for c in range(100):
            total += arr[r][c]

            if total > max_total:
                max_total = total

    # 각 열의 합
    for c in range(100):
        total = 0
        for r in range(100):
            total += arr[r][c]

            if total > max_total:
                max_total = total

    # 좌 -> 우 대각선의 합
    total = 0
    for r in range(100):
        total += arr[r][r]

        if total > max_total:
            max_total = total

    # 우 -> 좌 대각선의 합
    total = 0
    for r in range(100):
            total += arr[r][99 - r]

            if total > max_total:
                max_total = total


    print(f'#{tc} {max_total}')
