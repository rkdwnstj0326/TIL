# 0 : 공간 / 1 : 기둥 / 2 : 경비병
# 상하좌우로 N만큼 관찰 가능
# 시야에 1(기둥)이 있으면 기둥뒤는인식하지 못함

import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]

    total = 0

    # + 모양으로
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    count = 0

    # 구역하나정하기 (2를찾기)
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 2:

                for d in range(4):
                    for k in range(1, N):
                        nr = r + dr[d] * k
                        nc = c + dc[d] * k
                        if 0 <= nr < N and 0 <= nc < N:
                            if arr[nr][nc] == 0:
                                arr[nr][nc] = 1
                            elif arr[nr][nc] == 1:
                                break

    for r in range(N):
        # print(r)
        for c in range(N):
            if arr[r][c] == 0:
                count += 1

    print(f'#{tc} {count}')



