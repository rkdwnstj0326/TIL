# import sys
# sys.stdin = open("2001_파리퇴치.txt", "r")

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N, M = map(int, input().split())

    arr = [list(map(int, input().split())) for _ in range(N)]

    

    max_m_arr = 0

    # range(N)으로 해서 틀림.... 범위 지정 잘 생각하자
    for r in range(N - M + 1):
        for c in range(N - M + 1):

            sum_m_arr = 0

            for dr in range(M):
                for dc in range(M):
                    sum_m_arr += arr[r + dr][c + dc]

                max_m_arr = max(max_m_arr, sum_m_arr)

    print(f'#{test_case} {max_m_arr}')


