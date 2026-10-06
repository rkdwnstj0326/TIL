import sys
sys.stdin = open("input.txt", "r")

T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    Ai = list(map(int, input().split()))

    c = 1

    for i in range(N - 1):
        diff = Ai[i] - Ai[i + 1]

        if Ai[i] <= Ai[i + 1]:
            c = 0

        if diff < 1 or diff > 3:
            c = 0

    print(f'#{tc} {c}')
