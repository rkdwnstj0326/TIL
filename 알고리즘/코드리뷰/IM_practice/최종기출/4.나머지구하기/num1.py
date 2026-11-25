# import sys
# sys.stdin = open('input.txt')

# T = int(input())
# for tc in range(1, T + 1):
#     N = int(input())
#     A = list(map(int, input().split()))

#     # 나머지의 합
#     total = 0

#     # 나눠지는 숫자
#     for i in range(N):
#         for j in range(N):
#             total += A[i] % A[j]

#     print(f'#{tc} {total}')



import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    A = list(map(int, input().split()))

    # 나머지 다 더할 합
    total = 0

    for i in range(N):
        for j in range(N):
            total += A[i] % A[j]

    print(f'#{tc} {total}')
