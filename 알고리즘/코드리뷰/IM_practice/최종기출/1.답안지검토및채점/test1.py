import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    answer = list(map(int, input().split()))

    # 학생들의 총점 저장 리스트
    score = []

    # 일단 학생들 한명씩 채점
    for i in range(N):
        student = list(map(int, input().split()))
        total = 0
        count = 0
        for j in range(M):
            if answer[j] == student[j]:
                count += 1
                total += count
            else:
                count = 0

        # 총점 저장
        score.append(total)

    result = max(score) - min(score)
    print(f'#{tc} {result}')