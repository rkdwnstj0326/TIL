import sys
sys.stdin = open('input.txt')

T = int(input())

for tc in range(1, T + 1):
    N, W1, W2 = map(int,input().split())
    arr = list(map(int, input().split()))

    # arr 정렬
    arr.sort()

    total = 0
    # 리스트 만들기! 탑 2개 만들어야하니까
    l1 = []
    l2 = []
    # while문 사용
    # 무거운 화물일수록 비용이 적게 드는 아래에 설치해야됨
    # 그래서 arr의 마지막 화물부터 pop으로 꺼내서 append함
    while arr:
        if len(l1) < W1:
            l1.append(arr.pop())
        if len(l2) < W2:
            l2.append(arr.pop())

    # 비용 계산
    for i in range(W1):
        add1 = l1[i] * (i + 1)
        total = total + add1
    for j in range(W2):
        add2 = l2[j] * (j + 1)
        total = total + add2

    print(f'#{tc} {total}')

    