import sys
sys.stdin = open('모두방문하기/input.txt')

T = int(input())

for tc in range(1, T + 1):
    N, S = map(int,input().split())
    points = list(map(int,input().split()))

    left = min(points)
    right = max(points)
    span = right - left

    detour = min(abs(S - left), abs(S - right))

    print(f'#{tc} {span + detour}')








    # T = int(input())
    # for tc in range(1, T + 1):
    #     N, S = map(int, input().split())
    #     points = list(map(int, input().split()))

    #     left = min(points)
    #     right = max(points)
    #     span = right - left

    #     detour = min(abs(S - left), abs(S - right))

    #     print(f'#{tc} {span + detour}')

# T = int(input())

# for tc in range(1, T + 1):
#     N, K = map(int, input().split())
#     towers = list(map(int, input().split()))

#     for _ in range(K):

#         max_idx = towers.index(max(towers))
#         min_idx = towers.index(min(towers))


#         if towers[max_idx] - towers[min_idx] <= 1:
#             break

#         towers[max_idx] -= 1
#         towers[min_idx] += 1

#     print(f'#{tc} {max(towers) - min(towers)}')