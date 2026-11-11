# import sys
# sys.stdin = open('input.txt')

# T = int(input())
# for tc in range(1, T + 1):
#     N = int(input())
#     farm = [list(map(int, input())) for _ in range(N)]

#     total = 0

#     # 센터 구하기(중심값?)
#     center = N // 2
#     # start, end 정하기
#     start = center
#     end = center

#     for r in range(N):
#         for c in range(start, end + 1):
#             total = total + farm[r][c]

#         if r < center:
#             start = start - 1
#             end = end + 1
#         else:
#             start = start + 1
#             end = end - 1
#     print(f'#{tc} {total}')

import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    arr = [list(map(int, input())) for _ in range(N)]

    total = 0

    # center 설정
    center = N // 2
    # start, end 설정
    start = center
    end = center

    for r in range(N):
        for c in range(start, end + 1):
            total = total + arr[r][c]

        if r < center:
            start -= 1
            end += 1
        else:
            start += 1
            end -= 1
    print(f'#{tc} {total}')






