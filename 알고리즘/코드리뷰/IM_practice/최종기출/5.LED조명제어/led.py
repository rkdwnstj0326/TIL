import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input()) # led 개수
    led = [0] + list(map(int, input().split())) # 원하는 led 상태
    # 1번에서 N번 led가 됨

    sw = [0] * (N + 1) # 현재 led상태

    count = 0 #버튼을 누른 횟수

    for i in range(1, N + 1): # 1번부터 N번 led에 대해 (i는 확인하고 있는 led의 번호)
        if sw[i] != led[i]: # 현재 led상태와 원하는 led상태가 다르면 해당 번호의 버튼을 누르겟다
            count += 1

            for j in range(i, N + 1, i): # i의 배수 j(상태가 바뀌는 led의 번호)
                sw[j] = 1 - sw[j]

    print(f'#{tc} {count}')
    