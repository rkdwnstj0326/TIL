# 일단 필요한 변수 : total (누적합 할 변수 total = 0), 

# N = 5
#            열 (c)
#         0 1 2 3 4

# 행 0        O        -> 2 ~ 2 ############# start : 2 end : 2
# 행 1      O O O      -> 1 ~ 3 ############# start : 1 end : 3
# 행 2    O O O O O    -> 0 ~ 4 #############  여기를 기준으로 
# 행 3      O O O      -> 1 ~ 3 ############# start : 2 end : 2
# 행 4        O        -> 2 ~ 2 ############# start : 1 end : 3

import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):

    N  = int(input()) # 농장의 크기. 예를 들면 5면 5*5라는거임

    farm = []

    for _ in range(N):
        row = list(map(int, input()))
        farm.append(row) # 만든 행을 farm에 넣음

    # print(farm)
    total = 0

    center = N // 2 
    # 이거는 행이나 열에서 항상 중간값임 이걸 기준으로 위 아래 나눠서 봐야댐
    # 그럼, 기준 행과 열을 찾았으니까 반복문으로 각 행부터 내려와야하는거아님?
    # 열의 범위는 center에 다다를 때 까지 start는 줄어들고 end는 늘어난다
    
    start = center # 기준값을 두는 것임. 
    end = center

    for r in range(N): # 일단 모든 행 보셈
        for c in range(start, end + 1): # 그 행에서 start부터 end까지 보겟슨
            total = total + farm[r][c] # 그 값을 total에 더하겟슨

            # start = start - 1
            # end = end + 1

        if r < center: 
            start = start - 1
            end = end + 1
        else:
            start = start + 1
            end = end - 1
        # 가운데 행 까지 넓히고 가운데 행을 지나면 좁힌다
        # 쒜에에엣

    print(f'#{tc} {total}')


 

