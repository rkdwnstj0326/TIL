# 그림과 같이 인덱스가 있는 10x10 격자에 빨간색과 파란색을 칠하려고 한다.

# N개의 영역에 대해 왼쪽 위와 오른쪽 아래 모서리 인덱스, 칠할 색상이 주어질 때,
# 칠이 끝난 후 색이 겹쳐 보라색이 된 칸 수를 구하는 프로그램을 만드시오.

# 주어진 정보에서 같은 색인 영역은 겹치지 않는다.

# [입력]

# 첫 줄에 테스트 케이스 개수 T가 주어진다.(1 ≤ T ≤ 50)
# 다음 줄부터 테스트케이스의 첫 줄에 칠할 영역의 개수 N이 주어진다.(2 ≤ N ≤ 30)
# 다음 줄에 왼쪽 위 모서리 인덱스 r1, c1, 오른쪽 아래 모서리 r2, c2와 색상 정보 color가 주어진다.(0 ≤ r1, c1, r2, c2 ≤ 9)
# color = 1(빨강), color = 2(파랑)

# [출력]
# 각 줄마다 "#T"(T는 테스트 케이스 번호)를 출력한 뒤, 답을 출력한다.

# 목표 : 빨간색과 파란색이 겹치는 구역인 보라색 구역 찾기?
# 구조 : 일단 10x10격자 만들어서 빨간색 하나 파란색 하나 만들어야함. 그리고 두개 겹치는 부분을
#       찾아서 보라색으로 칠해진 부분 count 해야할듯

import sys
sys.stdin = open("sample_input.txt")
from pprint import pprint

T = int(input())

# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for tc in range(1, T + 1):
    N = int(input())
    # arr = [list(map(int, input().split())) for _ in range(N)] 
    # [[2(r1), 2(c1), 4(r2), 4(c2), 1(color)], [3, 3, 6, 6, 2]]
    grid = [[0] * 10 for _ in range(10)]
    count = 0

    for _ in range(N):
        arr = list(map(int, input().split()))
        r1 = arr[0]
        r2 = arr[2]
        c1 = arr[1]
        c2 = arr[3]
        color = arr[4]

    #     주어진 범위만큼 도화지위에 색칠하기
    # 값을 할당하려면 [행][열] = 1 or 2이렇게주어져야하나
    # 반복문으로 [2,2] 부터 [4,4]까지의 영역에 1을넣어야댐
    # (2,2) (2,3) (2,4)
    # (3,2) (3,3) (3,4)
    # (4,2) (4,3) (4,4) -> 여기에는 다 1이 들어가야댐

        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                grid[r][c] = grid[r][c] + color # 여기서 arr씀;;;;;grid 써야하는데...
                # 처음에 grid[r][c] = color씀

                if grid[r][c] == 3:
                    count = count + 1

    # print(count)
    print(f"#{tc} {count}")
                
    # pprint(grid)















