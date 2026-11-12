import sys
sys.stdin = open('input.txt')

T = 10
for tc in range(1, T + 1):
    N = int(input())
    views = list(map(int, input().split()))