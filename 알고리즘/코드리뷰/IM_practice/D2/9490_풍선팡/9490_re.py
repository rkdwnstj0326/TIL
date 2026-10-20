# 종이 꽃가루가 들어있는 풍선이 M개씩 N개의 줄에 붙어있고, 
# 어떤 풍선을 터뜨리면 안에 든 종이 꽃가루 개수만큼 상하 좌우의 풍선이 추가로 터지게 되는 게임이 있다.

# 예를 들어 풍선에 든 꽃가루가 1개씩일 때, 가운데 풍선을 터뜨리면 상하좌우의 풍선이 추가로 1개씩 터지면서 총 5개의 꽃가루가 날리게 된다.

# NxM개의 풍선에 들어있는 종이 꽃가루 개수A가 주어지면, 
# 한 개의 풍선을 선택했을 때 날릴 수 있는 꽃가루의 합 중 최대값을 출력하는 프로그램을 만드시오.
# (3<=N, M<=100)

# 입력
# 첫 줄에 테스트케이스 수 T, 다음 줄부터 테스트케이스 별로 첫 줄에 N과 M, 이후 N줄에 걸쳐 M개씩 풍선에 든 종이 꽃가루 개수가 주어진다.


# 출력
# #과 테스트케이스 번호, 빈칸에 이어 종이 꽃가루의 최대 개수를 출력한다.

import sys
sys.stdin = open("input.txt", "r")

# N = 행 / M = 열


T = int(input())  #문제가 3개 들어있다.

for tc in range(1, T + 1):
    N, M = map(int, input().split())

    arr = [list(map(int, input().split())) for _ in range(N)]

         # 상 하 좌 우
    dr = [-1, 1, 0, 0]  # row, 행을 얼마나 움직일지
    dc = [0, 0, -1, 1]  # column, 열을 얼마나 움직일지

    max_sum = 0          # 최대값을 저장할 변수!! 현재까지 발견한 가장 큰 값을 저장하는 변수임

    for r in range(N):
        for c in range(M): # 배열에 있는 풍선을 하나도 빠짐없이 전부 터뜨린다.

            center = arr[r][c]

            total = center

            for d in range(4): # 방향 4개 (상하좌우)를 다 확인하는거
                for distance in range(1, center + 1): # if) center = 3이면, range(1,4) 
                                                      #그럼 distance는 1, 2, 3 즉 한칸, 두칸, 세칸 떨어진 풍선을 보는거임

                    nr = r + dr[d] * distance
                    nc = c + dc[d] * distance

                    if 0 <= nr < N and 0 <= nc < M: # 배열 바깥으로 나갔는지 검사해야댐
                        total += arr[nr][nc] # 배열 안에 있는 풍선이라면 그 풍선의 꽃가루 개수를 더한다

                        # 여기까지 하면 한 풍선에 대한 계산이 끝난거임
                        # 상 하 좌 우 + 중간 까지 한 total이 만들어짐
    
            if total > max_sum:
                max_sum = total

    print(f'#{tc} {max_sum}')
    

    