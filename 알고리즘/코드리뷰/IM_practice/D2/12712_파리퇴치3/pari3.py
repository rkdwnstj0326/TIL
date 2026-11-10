import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    max_total = 0

    # + 방향으로
    plus_dr = [-1, 1, 0, 0]
    plus_dc = [0, 0, -1, 1]
    # X 방향으로
    cross_dr = [-1, -1, 1, 1]
    cross_dc = [-1, 1, -1, 1]
    # 중앙 하나정하기
    for r in range(N):
        for c in range(N):
            plus_total = arr[r][c]
            cross_total = arr[r][c]
            # + 방향 다 더하기
            for d in range(4):
                for k in range(1, M):
                    nr = r + plus_dr[d] * k
                    nc = c + plus_dc[d] * k

                    if 0 <= nr < N and 0 <= nc < N:
                        plus_total += arr[nr][nc]
            # X 방향 다 더하기
            for d in range(4):
                for k in range(1, M):
                    nr = r + cross_dr[d] * k
                    nc = c + cross_dc[d] * k

                    if 0 <= nr < N and 0 <= nc < N:
                        cross_total += arr[nr][nc]
            # 최댓값 갱신
            if plus_total > max_total:
                max_total = plus_total
            if cross_total > max_total:
                max_total = cross_total
    print(f'#{tc} {max_total}')