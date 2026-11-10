# 첫줄 - 덤프 횟수
# 두번째 - 각 상자의 높이값
# 덤프란? 평탄화과정임
# 최고점 - 최저점의 차이를 구해야됨


import sys
sys.stdin = open('input.txt')

T = 10
for tc in range(1, T + 1):
    N = int(input())
    towers = list(map(int, input().split()))
    # print(N)
    # print(towers)

    # towers.sort()
    # print(towers)
    for _ in range(N):
        max_idx = towers.index(max(towers))
        min_idx = towers.index(min(towers))

        if towers[max_idx] - towers[min_idx] <= 1:
            break

        towers[max_idx] -= 1
        towers[min_idx] += 1

    print(f'#{tc} {max(towers) - min(towers)}')

