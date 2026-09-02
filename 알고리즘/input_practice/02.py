import sys

sys.stdin = open('02.txt')


# 1 2 3 4 5 => [1, 2, 3, 4, 5]
numbers = list(map(int, input().split()))

print(numbers)
