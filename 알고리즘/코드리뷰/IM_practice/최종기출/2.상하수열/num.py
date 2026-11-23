T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    A = list(map(int, input().split()))

    max_v = 0 # 상하수열의 최대 길이
    count = 0 # 상하수열의 길이
    for k in range(N - 2):
        if A[k] == A[k + 2]:
        # if A[k] - A[k + 1] == -1 * (A[k + 1] - A[k + 2]):
            count += 1
            max_v = max(count, max_v)
        else:
            count = 0

    print(f'#{tc} {max_v + 2}')

