import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range (1, T + 1):
    N = int(input())
    numbers = list(map(int, input().split()))

    total = 0

    for i in range(N): # 첫번째 숫자의 위치
        for j in range(N): # 두번째 숫자의 위치
            if i == j: # 둘다 같은 위치면 건너뛴다
                continue

            total += numbers[i] % numbers[j] # 서로 다른 위치라면 나머지를 구해서 더해야한다.

    print(f'#{tc} {total}')

# i	j	계산	total
# 0	0	같은 위치 → 건너뜀	0
# 0	1	2 % 5 = 2	2
# 0	2	2 % 7 = 2	4
# 1	0	5 % 2 = 1	5
# 1	1	같은 위치 → 건너뜀	5
# 1	2	5 % 7 = 5	10
# 2	0	7 % 2 = 1	11
# 2	1	7 % 5 = 2	13
# 2	2	같은 위치 → 건너뜀	13

[2]
# for tc in range(1, T + 1):
#     N = int(input())
#     numbers = list(map(int, input().split()))

    # total = 0

    # for i in range(N):
    #     for j in range(N):
    #         if i == j:
    #             continue

    #         total += numbers[i] % numbers[j]

    # print(f'#{tc} {total}')

[3]
# import sys
# sys.stdin = open('input.txt')

# T = int(input())

# for tc in range(1, 1 + T):
#     N = int(input())
#     numbers = list(map(int, input().split()))

#     total = 0

#     for i in range(N):
#         for j in range(N):
#             if i == j:
#                 continue

#             total += numbers[i] % numbers[j]

#     print(f'#{tc} {total}')
