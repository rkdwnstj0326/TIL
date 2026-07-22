# SWEA Input 예제 기반 map 함수 사용 예제

import sys

sys.stdin = open('input.txt')

T = int(input())

for _ in range(T):
    # '1 2 3' => ['1', '2', '3'] => [1, 2, 3]
    numbers = list(map(int, input().split()))
    print(numbers)
