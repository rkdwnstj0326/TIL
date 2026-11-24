T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    A = list(map(int, input().split()))

    max_v = 0 # 상하수열의 최대 길이
    count = 0 # 상하수열의 길이
    for k in range(N - 2): # 인덱스 주의! 두 칸 앞을 검사하기 때문
        if A[k] == A[k + 2]:
        # if A[k] - A[k + 1] == -1 * (A[k + 1] - A[k + 2]):
            count += 1 # 연속한 상하수열
            max_v = max(count, max_v) # 최대 길이 갱신
        else:
            count = 0 # 상하수열이 아니면 길이 초기화

    print(f'#{tc} {max_v + 2}')# + 2 소급. 스타트 지점 두개는 항상 길이에서 제외되기 때문임

