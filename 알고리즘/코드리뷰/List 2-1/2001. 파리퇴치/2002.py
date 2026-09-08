import sys
sys.stdin = open("input.txt", "r")

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.

for tc in range(1, T + 1):
    N, M = map(int,input().split())
    result= 0
    # print(N)
    # print(M)

    grid = [list(map(int,input().split())) for _ in range(N)]
    #그러면 파리채를 대체 몇번이나 쳐야하는가?
    #=> 기준좌표를 몇번 바꿔야하는가?
    #=> (0,0) -> (N-M+1,N-M+1) 까지 기준좌표를 잡고
    #for
    #for
    #if result < fly(r,c) :
    # result = fly(r,c) #최댓값 업데이트
    #print(result)

def fly(r, c):#해당영역에 파리채로 조져서 합을 구할거임
    sum = 0 #합을 구할거니까 일단 변수를 하나 만들어
    #가로세로 길이가 M인건 알겠는데(파리채의 가로세로길이)
    #그러면 우리가 내려칠 영역의 기준 좌표는 뭘까?
    # 저 빨간색 부분을 내리친다고하면
    # (1,1)에서 시작해서 (1+M,1+M) 사이로 구하면 되지않을까?
    # 그러면 
    for row_i in range(r,r+M):
        for col_i in range(c,c+M):
            sum += grid[row+_,col_i]
    return sum # 이러면 해당 영역의 파리새기들의 시체의 수를 구할수잇다