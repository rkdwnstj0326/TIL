import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    answer = list(map(int, input().split()))

    # 빈 리스트 생성
    scores = []

    # 학생 한명당
    for i in range(N):
        arr = list(map(int, input().split()))

        count = 0
        total = 0
        for j in range(M):
            if arr[j] == answer[j]:
                count += 1
                total += count
            else:
                count = 0

        # 리스트에 total 추가
        scores.append(total)
    # 최대 - 최소
    result = max(scores) - min(scores)

    print(f'#{tc} {result}')