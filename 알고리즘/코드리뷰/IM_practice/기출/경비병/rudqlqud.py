# 0 : 공간 / 1 : 기둥 / 2 : 경비병
# 상하좌우로 N만큼 관찰 가능
# 시야에 1(기둥)이 있으면 기둥뒤는인식하지 못함

import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]


    # + 모양으로
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    count = 0

    # 경비병의 위치를 찾는다 (2를 찾아야함)
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 2:

                # 경비병을 찾으면 상하좌우 탐색 시작
                for d in range(4):
                    # 각 방향으로 이동
                    for k in range(1, N):
                        nr = r + dr[d] * k
                        nc = c + dc[d] * k
                        # 배열 안에 있는가
                        if 0 <= nr < N and 0 <= nc < N:
                            # 빈 공간(0)이라면 1로 바꾼다
                            if arr[nr][nc] == 0:
                                arr[nr][nc] = 1
                            # 기둥(1)을 만나면 더 안봐도 되어서 탐색 중지
                            elif arr[nr][nc] == 1:
                                break
    # 0의 개수 세기
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                count += 1

    print(f'#{tc} {count}')



