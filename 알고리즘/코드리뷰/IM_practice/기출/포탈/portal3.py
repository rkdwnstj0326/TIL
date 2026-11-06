import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range (1, T + 1):
    N = int(input())
    portals = [0] + list(map(int, input().split()))

    포탈방문 = [0] * (N + 1)

    현재방 = 1
    포탈사용량 = 0

    while 포탈사용량 < N:
        포탈사용량 += 1

        if 포탈사용량 == 1:
            포탈방문[현재방] += 1

        else:



