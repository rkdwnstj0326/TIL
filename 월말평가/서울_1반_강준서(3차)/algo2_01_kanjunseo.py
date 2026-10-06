# import sys
# sys.stdin = open('algo2_sample_in.txt')

T = int(input())

for test_case in range(1, T + 1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range]
