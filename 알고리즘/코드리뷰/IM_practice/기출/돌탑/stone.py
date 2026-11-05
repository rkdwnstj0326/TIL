# import sys
# sys.stdin = open('input.txt')

# T = int(input())

# for tc in range(1, T + 1):
#     N, K = map(int, input().split())
#     towers = list(map(int, input().split()))

#     for _ in range(K):
#         # 가장 높은 탑과 낮은 탑의 위치 찾기
#         max_idx = towers.index(max(towers))
#         min_idx = towers.index(min(towers))

#         if towers[max_idx] - towers[min_idx] <= 1:
#             break

#         towers[max_idx] -= 1 # 가장 높은탑에서 하나 빼기
#         towers[min_idx] += 1 # 가장 낮은 탑에서 하나 더하기

#     print(f'#{tc} {max(towers) - min(towers)}')


import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, K = map(int, input().split())
    towers = list(map(int, input().split()))

    for _ in range(K):
        # max.idx = max(towers) #여기틀림
        # min.idx = min(towers)
        max_idx = towers.index(max(towers))
        min_idx = towers.index(min(towers))

        if towers[max_idx] - towers[min_idx] <= 1:
            # 가장 높은 탑과 가장 낮은 탑의 돌 개수 차이가 1 이하인지 확인하는 조건문
            # 그니까 돌을 더 옮겨야 할까 말아야 할까,,,판단
            # 차이가 2 이상 나면 -> 아직 줄일 수 있는 가능성이 있으니까 계속해라
            break

        towers[max_idx] -= 1
        towers[min_idx] += 1

    print(f'#{tc} {max(towers) - min(towers)}')
























