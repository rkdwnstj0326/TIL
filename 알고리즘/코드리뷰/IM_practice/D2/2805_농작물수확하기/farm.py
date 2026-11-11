import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    farm = [list(map(int, input())) for _ in range(N)]

    total = 0

    # 농장의 가운데 위치 구하기
    center = N // 2
    # start, end로 각 행에서 수확할 열의 범위를 정한다.
    start = center
    end = center

    for r in range(N):
        for c in range(start, end + 1):
            total = total + farm[r][c]
        # 가운데 행보다 위에 있을 때
        if r < center:
            start = start - 1
            end = end + 1
        # 가운데 행이거나 그 아래에 있을 때
        else:
            start = start + 1
            end = end - 1
                
    print(f'#{tc} {total}')

