# 1. + 형태로 분사될때
# 2. x 형태로 분사될때
# N : 배열크기 / M : 분사세기(각 방향으로 뿌려지는 칸 수) 
import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    max_total= 0

    # + 방향
    plus_dr = [-1, 1, 0, 0]
    plus_dc = [0, 0, -1, 1]
    # x 방향
    cross_dr = [-1, -1, 1, 1]
    cross_dc = [-1, 1, -1, 1]
    # 스프레이 중심 위치 정하기
    for r in range(N):
        for c in range(N):
            plus_total = arr[r][c] # arr[r][c] : 현재 중심 칸에 존재하는 파리의 개수
            cross_total = arr[r][c]
            # + 모양 계산
            for d in range(4):
                for k in range(1, M):
                    nr = r + plus_dr[d] * k
                    nc = c + plus_dc[d] * k
                    # 스프레이가 배열 밖으로 벗어나지 않았는지 확인 + 배열 안에 있다면 해당 칸의 파리 개수 더하기
                    if 0 <= nr < N and 0 <= nc < N:
                        plus_total += arr[nr][nc]
            # x 모양 계산
            for d in range(4):
                for k in range(1, M):
                    nr = r + cross_dr[d] * k
                    nc = c + cross_dc[d] * k

                    if 0 <= nr < N and 0 <= nc < N:
                        cross_total += arr[nr][nc]

            # 최대 파리 개수 갱신
            if plus_total > max_total:
                max_total = plus_total

            if cross_total > max_total:
                max_total = cross_total

    print(f'#{tc} {max_total}')




    

