# import sys
# sys.stdin = open('input.txt')

# T = int(input())
# for tc in range(1, T + 1):
#     N = int(input())
#     LED = [0] + list(map(int, input().split()))

#     # 현재 LED의 상태
#     switch = [0] * (N + 1)

#     # 버튼을 누르는 횟수
#     count = 0

#     for i in range(1, N + 1):
#         # switch랑 led랑 다르면 해당 버튼 누른다
#         if switch[i] != LED[i]:
#             count += 1

#             # i의 배수 j
#             for j in range(i, N + 1, i):
#                 switch[j] = 1 - switch[j]

#     print(f'#{tc} {count}')


# import sys
# sys.stdin = open('input.txt')

# T = int(input())
# for tc in range(1, T + 1):
#     N = int(input())
#     LED = [0] + list(map(int, input().split()))

#     switch = [0] * (N + 1)

#     count = 0

#     for i in range(1, N + 1):
#         if switch[i] != LED[i]:
#             count += 1

#             for j in range(i, N + 1, i):
#                 switch[j] = 1 - switch[j]

#     print(f'#{tc} {count}')





import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    LED = [0] + list(map(int, input().split()))

    switch = [0] * (N + 1)

    count = 0

    for i in range(1, N + 1):
        if switch[i] != LED[i]:
            count += 1

            for j in range(i, N + 1, i):
                switch[j] = 1 - switch[j]

    print(f'#{tc} {count}')
    


















