import sys
sys.stdin = open("input.txt", "r")

T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    Ai = list(map(int, input().split()))

    count = 0

    for i in range(N - 1):
        if Ai[i] <= Ai[i + 1]:
            count = count + 1

    if count <= 1:
        result = 1
    else:
        result = 0

    print(f'#{tc} {result}')