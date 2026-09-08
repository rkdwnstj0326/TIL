# ------------------------------------------------------------
# 03. Stack 응용 1 - 괄호 검사 (딕셔너리 방식)
# ------------------------------------------------------------
# [학습 목표]
#   02번의 if-elif 3줄은 결국 "닫는 괄호 -> 짝이 되는 여는 괄호" 라는
#   '대응 관계'를 코드로 늘어놓은 것이다.
#   이 대응 관계를 딕셔너리에 담으면 if 3개가 비교 한 줄로 줄어든다.
#
#     if char == ')' and open_char != '(':  ...
#     elif char == ']' and open_char != '[': ...   =>   if matches[char] != open_char:
#     elif char == '}' and open_char != '{': ...
#
#   괄호 종류가 늘어나도 딕셔너리에 한 줄만 추가하면 되는 이유를 설명할 수 있다.
# ------------------------------------------------------------

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.stdin = open(BASE_DIR / 'input.txt')


def check_brackets_map(string):
    # 닫는 괄호를 키로, 짝이 되는 여는 괄호를 값으로 매핑
    matches = {
        ')': '(',
        ']': '[',
        '}': '{',
    }
    stack = []

    for char in string:
        # TODO 1) 여는 괄호인지 확인하는 조건을 작성하세요.
        #   힌트: 여는 괄호는 딕셔너리의 '값' 쪽에 있다. matches.values() 사용
        #         (그냥 '([{' 문자열을 써도 된다)
        if None:
            # TODO 2) 여는 괄호를 스택에 넣으세요.
            pass

        # TODO 3) 닫는 괄호인지 확인하는 조건을 작성하세요.
        #   힌트: 닫는 괄호는 딕셔너리의 '키' 쪽에 있다. matches.keys() 사용
        elif None:
            # 닫는 괄호가 왔는데 스택이 비어있다면 -> 잘못된 경우
            if len(stack) == 0:
                return -1

            # TODO 4) 스택에서 여는 괄호를 하나 꺼내세요.
            open_char = None

            # TODO 5) 꺼낸 여는 괄호가 현재 닫는 괄호의 올바른 짝인지 확인하세요.
            #   힌트: matches[char] 가 '현재 닫는 괄호의 올바른 짝꿍' 이다.
            #         이것과 open_char 가 다르면 실패
            if None:
                return -1

        # 그 외 문자는 무시한다.

    # TODO 6) 모든 반복이 끝난 후 스택이 비어있는지 확인해 결과를 반환하세요.
    #   힌트: 삼항 연산자로 한 줄로 쓸 수도 있다.
    #         return 1 if 조건 else -1
    return -1


T = int(input())
for tc in range(1, T + 1):
    line = input()
    print(f'#{tc} {check_brackets_map(line)}')

# [기대 출력]  output.txt 참고 (02번과 결과가 완전히 같아야 한다)
#   #1 1
#   #2 -1
#   #3 1


print('\n' + '=' * 55 + '\n')


# ------------------------------------------------------------
# [딕셔너리 사용법 확인] 실행해서 눈으로 익히기
# ------------------------------------------------------------
matches = {')': '(', ']': '[', '}': '{'}

print('=== matches 딕셔너리 뜯어보기 ===')
print(f'  matches           : {matches}')
print(f'  matches.keys()    : {list(matches.keys())}    <- 닫는 괄호들')
print(f'  matches.values()  : {list(matches.values())}    <- 여는 괄호들')
print(f"  matches[')']      : {matches[')']!r}          <- ')' 의 짝꿍")
print(f"  ']' in matches    : {']' in matches}         <- in 은 기본적으로 '키'를 검사")
print(f"  '[' in matches    : {'[' in matches}        <- 여는 괄호는 키가 아니므로 False!")

# [주의] char in matches 는 char in matches.keys() 와 같은 뜻이다.
#        값(여는 괄호)을 검사하려면 반드시 matches.values() 를 명시해야 한다.
#        TODO 1) 에서 실수하기 쉬운 지점이다.


print('\n' + '=' * 55 + '\n')


# ------------------------------------------------------------
# [두 방식 비교] 02번과 결과가 같은지 직접 검증
# ------------------------------------------------------------
def check_brackets_if(string):
    """02번의 if-elif 방식 (비교용 - 이미 완성되어 있습니다)"""
    stack = []
    for char in string:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if len(stack) == 0:
                return -1
            open_char = stack.pop()
            if (
                (char == ')' and open_char != '(')
                or (char == ']' and open_char != '[')
                or (char == '}' and open_char != '{')
            ):
                return -1
            # if char == ')' and open_char != '(':
            #     return -1
            # elif char == ']' and open_char != '[':
            #     return -1
            # elif char == '}' and open_char != '{':
            #     return -1
    return 1 if len(stack) == 0 else -1


test_cases = [
    '(12[3]{45}[])',
    '([{)]}999',
    '([]{})((12345){[67]})',
    '(((',
    ')))',
    '',
    '1234',
]

print('=== if-elif 방식 vs 딕셔너리 방식 ===')
print(f'  {"입력":<26} | if-elif | dict | 일치')
print(f'  {"-" * 26} | ------- | ---- | ----')
for case in test_cases:
    a = check_brackets_if(case)
    b = check_brackets_map(case)
    same = 'O' if a == b else 'X'
    print(f'  {case!r:<26} | {a:^7} | {b:^4} | {same:^4}')

# [목표] '일치' 열이 전부 O 가 되어야 완성이다.
#
# [생각해보기] 빈 문자열('')과 괄호 없는 문자열('1234')의 정답은 무엇일까?
#              "짝이 맞지 않는 괄호가 없다" 는 조건을 만족하는지 따져보자.


print('\n' + '=' * 55 + '\n')


# ------------------------------------------------------------
# [스스로 점검하기]
# ------------------------------------------------------------
# Q1. 딕셔너리를 {'(': ')'} 처럼 반대로 만들면 무엇이 불편해질까?
#     (힌트: pop 한 직후에 무엇을 바로 조회하고 싶은가?)
#
# Q2. 여는 괄호 검사를 char in matches 로 쓰면 왜 항상 False 일까?
#
# Q3. 괄호 종류에 < > 를 추가하려면 각 방식에서 코드를 몇 줄 고쳐야 할까?
#     (02번 방식 vs 03번 방식을 비교해 보자)
#
# Q4. 같은 문제의 두 풀이가 다른 답을 낸다면, 무엇을 먼저 의심해야 할까?
