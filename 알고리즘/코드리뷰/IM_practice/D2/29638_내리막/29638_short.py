T = int(input())
 
for tc in range(1, T+1):
    N = int(input())
    Ai = list(map(int, input().split()))
 
    c = 1
    # 처음에는 감소한다고 가정하기 때문에 c = 1로 두고, 감소 조건을 어길 때만 0으로 바꾼다
    # 그러면 숫자가 하나인 경우에도 자동으로 1이 됨
 
    for i in range(N - 1): # i를 0부터 N-2까지 바꾸면서 반복하겟음
        if Ai[i] <= Ai[i + 1]:
            c = 0
 
 
    print(f'#{tc} {c}')