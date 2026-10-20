import sys
sys.stdin = open("input.txt")

T = int(input())

for tc in range(1, T + 1):
    word = input()

    if word == word[::-1]:
        # 원래 단어랑 뒤집은 단어랑 같으면 회문이다.
        # word[::-1]은 단어를 뒤집은거임
        answer = 1

    else:
        answer = 0

    print(f'#{tc} {answer}')