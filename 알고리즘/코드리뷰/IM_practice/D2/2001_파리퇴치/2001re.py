import sys
sys.stdin = open("input.txt")

T = int(input())

for tc in range(1, T + 1):
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    # for반복문 4번

    max_total = 0

    for r in range(N - M + 1):
        for c in range(N - M + 1):

            total = 0

            for i in range(r, r + M):
                for j in range(c, c + M):
                    total += arr[i][j]

            if total > max_total:
                max_total = total


    print(f'#{tc} {max_total}')
