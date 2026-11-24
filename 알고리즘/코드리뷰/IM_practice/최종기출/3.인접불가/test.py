T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    txt = input()

    # 내가 지워야할 글자 수
    count = 0
    for i in range(N - 1):
        if txt[i] in 'ab' and txt[i + 1] in 'ab':
            count += 1

    print(f'#{tc} {count}')