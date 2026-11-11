import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, W1, W2 = map(int, input().split())
    arr = list(map(int, input().split()))

    total = 0

    # arr 정렬하기
    arr.sort()
    # l1 l2 만들기
    l1 = []
    l2 = []
    # l1, l2 채우기
    while arr:
        if len(l1) < W1:
            l1.append(arr.pop())
        if len(l2) < W2:
            l2.append(arr.pop())
    # 무게 계산하기
    for i in range(W1):
        add1 = l1[i] * (i + 1)
        total = total + add1
    for j in range(W2):
        add2 = l2[j] * (j + 1)
        total = total + add2

    print(f'#{tc} {total}')
    