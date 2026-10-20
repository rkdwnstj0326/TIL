import sys
sys.stdin = open("sample_input.txt")

# 묶음개수 = N-M+1

T = int(input())

for tc in range(1, T + 1):
    N, M = map(int, input().split())
    arr = list(map(int, input().split()))

    # 첫번째 묶음의 합을 구하려면?
    # total = arr[0] + arr[1] + arr[2] 이건데, 이걸 매번 작성할 수 없으니까 for문으로 반복 돌리기
    
    for i in range(N - M + 1):
        total = 0

        for j in range(i, i + M):
            total = total + arr[j]


        if i == 0:
            max_total = total
            min_total = total

        else:
            if max_total < total:
                max_total = total

            if min_total > total:
                min_total = total

    answer = max_total - min_total

    print(f'#{tc} {answer}')