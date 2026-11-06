import sys
sys.stdin = open('모두방문하기/input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, S = map(int, input().split())
    points = list(map(int, input().split()))

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
#     N, S = map(int, input().split())
#     points = list(map(int, input().split()))

#     left = min(points)
#     right = max(points)
#     span = right - left

#     detour = min(abs(S - left), abs(S - right))

#     print(f'#{tc} {span + detour}')

