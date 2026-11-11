# + 모양
# p : 범위

import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    # dr, dc 설정
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    max_total = 0

    # 어디 터지는지 정하기
    for r in range(N):
        for c in range(M):
            bomb = arr[r][c] # arr[r][c]에 적혀있는 숫자가 터지는 범위 + 위력임
            total = bomb

            for d in range(4):
                for k in range(1, bomb + 1): # k는 현재 위치에서 이동하는 거리를 의미해서 +1을 해줘야댐
                    nr = r + dr[d] * k
                    nc = c + dc[d] * k
                    if 0 <= nr < N and 0 <= nc < M:
                        total = total + arr[nr][nc]

            if total > max_total:
                max_total = total

    print(f'#{tc} {max_total}')


