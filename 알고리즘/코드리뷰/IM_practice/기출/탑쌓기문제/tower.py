import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, W1, W2 = map(int, input().split())
    arr = list(map(int, input().split()))

    # arr를 정렬
    arr.sort()
    # print(arr)
    total = 0

    # 리스트만들기
    l1 = []
    l2 = []

    # append(arr.pop()) 써서 했던거같은데뭐더라
    while arr: # arr 리스트에 화물이 하나라도 있으면 계쏙 반복
        if len(l1) < W1: # 화물 개수가 3개보다 적으면
            l1.append(arr.pop()) # arr의 마지막 화물(제일큰거)꺼내서 첫 탑에 추가
        if len(l2) < W2:
            l2.append(arr.pop())
        # if를 각각 작성해야됨 -> 한번 반복할 때 l1에도 넣고 l2에도 넣고.

    # 비용 구하기
    for i in range(W1): 
        add1 = l1[i] * (i + 1)
        total = total + add1
    for j in range(W2):
        add2 = l2[j] * (j + 1)
        total = total + add2

    print(f'#{tc} {total}')