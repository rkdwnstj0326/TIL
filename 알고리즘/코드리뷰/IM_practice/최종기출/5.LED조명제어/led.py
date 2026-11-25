import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    led = [0] + list(map(int, input().split()))
    # 1번에서 N번 led가 됨

    sw = [0] * (N + 1) # N번까지의 초기상태

    count = 0

    for i in range(1, N + 1): # 1번부터 N번 led에 대해
        if sw[i] != led[i]: # 다르면 조작 필요
            count += 1

            for j in range(i, N + 1, i): # i의 배수 j
                sw[j] = 1 - sw[j]

    print(f'#{tc} {count}')