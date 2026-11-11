# 0 : 공간 / 1: 기둥 / 2 : 경비병
# 상하좌우로 N만큼 관찰 가능하다
# 시야에 1(기둥) 있으면 기둥 뒤에는 인식하지 못한다

# import sys
# sys.stdin = open('input.txt')

# T = int(input())
# for tc in range(1, T + 1):
#     N = int(input())
#     arr = [list(map(int, input().split())) for _ in range(N)]

#     # 배열 만들기
#     dr = [-1, 1, 0, 0]
#     dc = [0, 0, -1, 1]

#     count = 0
#     # 경비병 찾기 (2를 찾아야댐)
#     for r in range(N):
#         for c in range(N):
#             if arr[r][c] == 2:
#                 # 2 를 찾으면 상하좌우로 터뜨리기
#                 for d in range(4):
#                     for k in range(1, N):
#                         nr = r + dr[d] * k
#                         nc = c + dc[d] * k
#                         # N*N 배열 안에 있는지 확인
#                         if 0 <= nr < N and 0 <= nc < N:
#                             # 빈 공간(0)이면 기둥(1)로 바꾼다
#                             if arr[nr][nc] == 0:
#                                 arr[nr][nc] = 1
#                             # 기둥(1)이 있으면 break
#                             elif arr[nr][nc] == 1:
#                                 break
#     # 0 개수 세기
#     for r in range(N):
#         for c in range(N):
#             if arr[r][c] == 0:
#                 count += 1

#     print(f'#{tc} {count}')
#############################################################################
# 0 : 공간 / 1: 기둥 / 2 : 경비병
# 상하좌우로 N만큼 관찰 가능하다
# 시야에 1(기둥) 있으면 기둥 뒤에는 인식하지 못한다

# 1. 처음에 dr dc 배열 설정
# 2. arr에서 경비병 찾기(2를 찾아야함)
# 3. 2를 찾으면 상하좌우로 탐색
# 4. 각 방향으로 이동 nr nc  정하기
# 5. 배열 안에 있는지 확인 (크기확인)
# 6. 빈 공간(0)이면 1로 바꾼다
# 7. 기둥(1)을 만나면 뒤를 더 확인 안해도 된까 break
# 8. 0의 개수 카운트

import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]

    # dr, dc 배열 만들기
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    count = 0

    # 경비병 찾기
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 2:
            # 상하좌우
                for d in range(4):
                    for k in range(1, N):
                        nr = r + dr[d] * k
                        nc = c + dc[d] * k
                        # 배열 크기 확인
                        if 0 <= nr < N and 0 <= nc < N:
                            # 0 이면 1로 바꾼다
                            if arr[nr][nc] == 0:
                                arr[nr][nc] = 1
                            elif arr[nr][nc] == 1:
                                break

    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                count += 1
    print(f'#{tc} {count}')

