# 흰색(단어 O) : 1 / 검은색(단어 X) : 0
# N = 퍼즐 크기 / K = 특정 길이

import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, K = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    total = 0

    # 가로 찾기
    for r in range(N):
        count = 0
        for c in range(N):
            if arr[r][c] == 1:
                count += 1
            else:
                if count == K:
                    total += 1
                count = 0
        if count == K:
            total += 1

    # 세로 찾기
    for c in range(N):
        count = 0
        for r in range(N):
            if arr[r][c] == 1:
                count += 1
            else:
                if count == K:
                    total += 1
                count = 0
        if count == K:
            total += 1

    print(f'#{tc} {total}')

                

