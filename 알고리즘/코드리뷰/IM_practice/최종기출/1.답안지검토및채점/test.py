T = int(input())

for tc in range(1, T + 1):
    N, M = map(int, input().split())
    correct = list(map(int, input().split()))
    score = []

    for _ in range(N):
        student = list(map(int, input().split()))
        total = 0
        cnt = 0
        for i in range(M):
            if correct[i] == student[i]:
                cnt += 1
                total += cnt
            else:
                cnt = 0
        score.append(total)
    diff = max(score) - min(score)
    print(f'#{tc} {diff}')
                    
    