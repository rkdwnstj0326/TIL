# import sys
# sys.stdin = open('algo1_sample_in.txt')

T = int(input())

for test_case in range(1, T + 1):
    N = int(input())

    arr = list(map(int,input().split()))

    # for num in range(1, T + 1):
    if N % 2 == 1:
        arr[0] + arr[4] > arr[1] + arr[3]
        print(f'#{test_case} {1}')

    else:
        print(f'#{test_case} {0}')

# 계속 증가하면 1 / 증가하지 않으면 0
# 홀수개일 때 -> 중간 값 뺀다. / 짝수개일 때 -> 짝이 있으므로 무시 안함.
# 아 근데 중간에 남는지 볼려면 N을 2로 나눴을 때 나머지가 1이어야 하는데 이걸 어디다 뒁야하지

