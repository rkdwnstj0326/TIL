# 2차원 배열에서 M*M 크기의 파리채를 한 칸씩 이동시키면서, 
# 파리 개수의 합이 가장 큰 위치를 찾는 문제임

# for문을 총 4번을 사용해야함
# 1. 파리채를 위에서 아래로 이동한다
# 2. 파리채를 왼쪽에서 오른쪽으로 이동한다
# 3. 파리채 안의 행을 탐색한다.
# 4. 파리채 안의 열을 탐색한다.

import sys
sys.stdin = open("input.txt")

T = int(input())

for tc in range(1, T + 1):
    N, M = map(int, input().split())

    arr = [list(map(int, input().split())) for _ in range(N)] #2차원 배열을 만드는과정

    # 그렇다면 파리채를 놓을 자리는 어케 구해여?
    # 배열의 위치:  0  1  2  3  4

    # 첫 번째:     ■  ■  ■  □  □
    # 두 번째:     □  ■  ■  ■  □
    # 세 번째:     □  □  ■  ■  ■
    # 그래서  N - M + 1이 나옴
    max_total = 0

    for r in range(N - M + 1):
        for c in range(N - M + 1):
            total = 0 
            # total은 지금 파리채를 내려친 위치에서 잡은 파리의 수
            # total = 0을 여기 두는 이유는 파리채를 새로운 위치에 좋을 때 마다 초기화 하려고

            for i in range(r, r + M): # i는 파리채 안에서 탐색하는 행
                for j in range(c, c + M): # j는 파리채 안에서 탐색하는 열
                    total = total + arr[i][j]

            if total > max_total:
                max_total = total

    print(f'#{tc} {max_total}')
            