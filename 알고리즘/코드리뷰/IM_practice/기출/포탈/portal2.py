import sys
sys.stdin = open('input.txt')

T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    portals = [0] + list(map(int, input().split()))

    visit_counts = [0] * (N + 1)

    현재방 = 1
    포탈사용량 = 0

    while 현재방 < 5:
        포탈사용량 += 1

        if 현재방 == 1:
            다음방 = 2

        else:
            visit_counts[현재방] += 1

            if visit_counts[현재방] == 1:
                다음방 = portals[현재방]

            else:
                다음방 = 현재방 + 1

        현재방 = 다음방
    print(f'#{tc} {포탈사용량}')
