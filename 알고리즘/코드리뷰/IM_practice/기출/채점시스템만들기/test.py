import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    answer = list(map(int, input().split())) # 정답지

    # 학생들의 총점 저장 리스트
    scores = []

    # 학생들 한명씩 채점
    for i in range(N):

        arr = list(map(int, input().split()))
        total = 0
        count = 0
        # 문제 확인
        for j in range(M):
            # 학생답 = 정답
            if arr[j] == answer[j]:
                count += 1
                total += count
            # 학생답 != 정답
            else:
                count = 0
        # 총점 저장
        scores.append(total)
    # 최고점과최저점 차이
    result = max(scores) - min(scores)

    print(f'#{tc} {result}')



