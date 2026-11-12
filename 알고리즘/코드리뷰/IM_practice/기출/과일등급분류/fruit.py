import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, lo, hi = map(int, input().split())
    weight = list(map(int, input().split()))

    # 정렬하기
    weight.sort()
    # print(weight)
    