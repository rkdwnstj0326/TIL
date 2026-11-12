import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N, M = map(int, input().split())
    answer = list(map(int, input().split()))

    scores = []

    # 학생들 한명씩 채점
    for i in range(N):
        arr = list(map(int, input().split())) #학생 1번부터 답안지 받음
        total = 0 # 점수 총점
        count = 0 # 점수 계산을 위해서 필요
        # 문제 확인
        for j in range(M):
            # 정답일때
            if arr[j] == answer[j]: # i는 학생을 뜻하는거여서 j를 써야댐
                count += 1
                total += count
            # 정답아닐때
            else:
                count = 0

        # 총점 저장
        scores.append(total)
    # 최고 - 최저
    result = max(scores) - min(scores)

    print(f'#{tc} {result}')


