import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int,input().split())
    answer = list(map(int, input().split()))

    # 점수 담을 리스트 생성
    scores = []

    # 학생 1명씩
    for i in range(N):
        arr = list(map(int, input().split()))
        total = 0
        count = 0
        for j in range(M):
            if arr[j] == answer[j]:
                count += 1
                total += count
            else:
                count = 0
        # 총점 저장
        scores.append(total)

    result = max(scores) - min(scores)

    print(f'#{tc} {result}')