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