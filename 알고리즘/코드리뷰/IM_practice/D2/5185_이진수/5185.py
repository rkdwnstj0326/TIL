# 16진수 1자리는 2진수 4자리로 표시된다.
# N자리 16진수가 주어지면 각 자리 수를 4자리 2진수로 표시하는 프로그램을 만드시오.
# 단, 2진수의 앞자리 0도 반드시 출력한다.
# 예를 들어 47FE라는 16진수를 2진수로 표시하면 다음과 같다.
# 0100011111111110


# [입력]
# 첫 줄에 테스트케이스의 수 T가 주어진다. 1<=T<=50
# 다음 줄부터 테스트 케이스의 별로 자리 수 N과 N자리 16진수가 주어진다. 1<=N<=100
# 16진수 A부터 F는 대문자로 표시된다.
 
# [출력]
# 각 줄마다 "#T" (T는 테스트 케이스 번호)를 출력한 뒤, 답을 출력한다.

import sys
sys.stdin = open('sample_input.txt')

T = int(input())

# 문제에 따라 이 숫자 4개만 변경하면 됨

FROM = 16 # 입력진수
TO = 2 # 출력진수
GROUP = 1 # 몇 자리 씩 끊을 지
WIDTH = 4 # 출력 최소 자리수

for tc in range(1, T + 1):
    result = ''

    # 그리고 이 부분을 수정할 줄 알아야함
    N, hex_text = input().split()

    for i in range(0, int(N), GROUP):
        h = hex_text[i:i+GROUP]
    #여기까지

        integer = int(h, FROM)
        binary = format(integer, {2:'b', 8:'o', 10:'d', 16:'X'}[TO])
        result += binary.zfill(WIDTH)

    print(f'#{tc} {result}')

