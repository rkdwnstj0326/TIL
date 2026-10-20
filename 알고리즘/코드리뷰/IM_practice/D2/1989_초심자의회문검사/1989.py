import sys
sys.stdin = open("input.txt")

T = int(input())

for tc in range(1, T + 1):
    word = input()
    answer = 1
    # 일단 입력된 단어가 무조건 회문이라고 생각한다.

    for i in range(len(word) // 2):
        #len(word)라고 해도 되는데 굳이 len(word)//2 라고 하는 이유는 두번일 안하려고?
        if word[i] != word[len(word) - 1 - i]:
            # 만약에 i번째랑 word[단어길이 - 1 - i]가 같지 않으면 회문이 아니다
            # len(word)-1-i -> 맨끝번째 순서에서 차근차근 앞으로 옴
            answer = 0

            break

    print(f'#{tc} {answer}')

