import sys
sys.stdin = open("input.txt")

# 각 행의 합(row) : row를 고정시키고 c를 늘려야 한다.
# 각 열의 합 : col을 고정시키고 r을 늘려야함
# 각 대각선의 합
# 이 3개를 다 구해야함 그리고 거기서 제일 최대값 구해야함

# T = int(input())

T = 10 #tc가 무조건 10개 라고 정해져 있음

for tc in range(1, T + 1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(100)] #100x100배열 받기

    max_total = 0

    # 각 행의 합

    for r in range(100):
        total = 0
        for c in range(100):
            total = total + arr[r][c]

        max_total = max(max_total, total)

    # 각 열의 합
    for c in range(100):
        total2 = 0
        for r in range(100):
            total2 = total2 + arr[r][c]

        max_total = max(max_total, total2)

    # 대각선의 합(오른쪽으로 내려가는 대각선)
    total3 = 0

    for r in range(100):
        total3 = total3 + arr[r][r]
    max_total = max(max_total, total3)

    # 대각선의 합(오른쪽으로 올라가는 대각선)
    total4 = 0

    for r in range(100):
        total4 = total4 + arr[r][99-r]
    max_total = max(max_total, total4)

    print(f"#{tc} {max_total}")            



