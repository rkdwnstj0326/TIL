import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    answer = list(map(int, input().split()))

    score = []
    for i in range(N):
        student = list(map(int, input().split()))

        count = 0
        total = 0
        for j in range(M):
            if answer[j] == student[j]:
                count += 1
                total += count
            else:
                count = 0
        score.append(total)
    result = max(score) - min(score)
    print(f'#{tc} {result}')