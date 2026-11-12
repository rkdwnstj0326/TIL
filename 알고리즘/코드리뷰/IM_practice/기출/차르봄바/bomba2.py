import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    # dr dc 정하기
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    max_total = 0

    # 중심위치 정하기
    for r in range(N):
        for c in range(M):
            bomb = arr[r][c]
            total = bomb

            for d in range(4):
                for k in range(1, bomb + 1):
                    nr = r + dr[d] * k
                    nc = c + dc[d] * k
                    if 0 <= nr < N and 0 <= nc < M:
                        total = total + arr[nr][nc]

            if total > max_total:
                max_total = total
    print(f'#{tc} {max_total}')

