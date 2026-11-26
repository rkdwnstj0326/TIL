import sys
sys.stdin = open('input.txt')

T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    txt = input()

    count = 0

    for i in range(N - 1):
        if txt[i] in 'ab' and txt[i + 1] in 'ab':
            count += 1

    print(f'#{tc} {count}')