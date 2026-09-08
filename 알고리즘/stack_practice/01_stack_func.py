# ------------------------------------------------------------
# 01. Stack 구현 (함수 버전)
# ------------------------------------------------------------
# [비유] 프링글스 통
#   맨 나중에 넣은 과자를 맨 먼저 꺼낸다. 중간 것을 빼내려면? 위부터 다 꺼내야 한다.
#   => 후입선출 (LIFO, Last-In-First-Out)
#
# [Top] 스택의 가장 위(마지막) 데이터의 위치.
#       파이썬 리스트에서는 인덱스 [-1] 이 곧 top 이다.
#
# [학습 목표]
#   연산       | 설명                              | 리스트 메서드      | 복잡도
#   ---------- | --------------------------------- | ------------------ | ------
#   push       | 맨 위에 데이터를 넣는다           | list.append(item)  | O(1)
#   pop        | 맨 위 데이터를 꺼내고 반환한다    | list.pop()         | O(1)
#   peek       | 맨 위 데이터를 확인만 한다        | list[-1]           | O(1)
#   is_empty   | 비어있는지 확인한다               | len(list) == 0     | O(1)
#
#   위 네 연산을 직접 구현하고, 왜 전부 O(1) 인지 설명할 수 있다.
# ------------------------------------------------------------

# 1. 스택으로 사용할 빈 리스트 생성
stack = []


# 2. push 연산: 리스트의 가장 끝에 데이터를 추가
def push(item):
    # TODO 1) 리스트의 맨 뒤에 item 을 추가하세요.
    #   힌트: 리스트의 append 메서드
    pass

    print(f'Push({item}) -> 현재 스택: {stack}')


# 3. pop 연산: 리스트의 가장 끝 데이터를 꺼내고 반환
def pop():
    # TODO 2) 스택이 비어있는지 확인하는 조건을 작성하세요. (Underflow 방지)
    #   힌트: 리스트의 길이가 0인지 확인
    if None:
        print('Stack Underflow! 스택이 비어있습니다.')
        return None
    else:
        # TODO 3) 리스트의 마지막 요소를 꺼내고 그 값을 item 에 담으세요.
        #   힌트: list.pop() 은 마지막 요소를 '제거하고 그 값을 반환' 한다.
        item = None

        print(f'Pop() -> 꺼낸 요소: {item}, 현재 스택: {stack}')
        return item


# 4. peek 연산: 가장 끝 데이터를 확인만 함 (삭제하지 않음)
def peek():
    if len(stack) == 0:
        print('스택이 비어있습니다.')
        return None

    # TODO 4) 맨 마지막 요소를 반환하세요. (꺼내면 안 됩니다!)
    #   힌트: 마지막 요소의 인덱스는 -1
    return None


# 5. is_empty 연산: 비어있으면 True
def is_empty():
    # TODO 5) 스택이 비어있는지 True / False 로 반환하세요.
    #   힌트: 비교 결과 자체가 True 또는 False 다. if 문이 필요 없다.
    return None


# --- 실행 테스트 ---
print('=== 스택 테스트 시작 ===')
push(10)
push(20)
push(30)

print(f'\n현재 top: {peek()}')  # 30 이 나와야 한다

pop()  # 30 제거
pop()  # 20 제거
pop()  # 10 제거
pop()  # Underflow 발생

print(f'\nis_empty: {is_empty()}')  # True 가 나와야 한다


print('\n' + '=' * 55 + '\n')


# ------------------------------------------------------------
# [동작 과정 시각화] 스택을 프링글스 통처럼 세워서 그려보기
# ------------------------------------------------------------
def draw_stack(items):
    """리스트를 아래에서 위로 쌓인 스택 모양으로 출력"""
    if len(items) == 0:
        print('  (비어 있음)')
        print('  +------+')
        return

    # 리스트의 뒤쪽이 위(top)이므로 거꾸로 그린다
    for i in range(len(items) - 1, -1, -1):
        mark = '  <- top' if i == len(items) - 1 else ''
        print(f'  | {items[i]:^4} |{mark}')

    print('  +------+')


print('=== push 과정 ===')
demo = []
for value in [10, 20, 30]:
    demo.append(value)
    print(f'push({value})')
    draw_stack(demo)
    print()

print('=== pop 과정 ===')
while demo:
    item = demo.pop()
    print(f'pop() -> {item}')
    draw_stack(demo)
    print()

# [읽어보기] 이 시각화 코드는 완성되어 있습니다. 실행 결과를 보며
#            리스트의 '오른쪽 끝' 이 그림에서는 '맨 위' 라는 대응을 확인하세요.
#
#   push(30) 직후의 모습
#     |  30  |  <- top      <- stack[-1]
#     |  20  |
#     |  10  |              <- stack[0] (바닥)
#     +------+


print('=' * 55 + '\n')


# ------------------------------------------------------------
# [Overflow & Underflow]
# ------------------------------------------------------------
# Overflow  : 꽉 찬 스택에 데이터를 더 넣으려 할 때 발생.
#             파이썬 리스트는 크기가 자동으로 늘어나므로 거의 발생하지 않는다.
# Underflow : 텅 빈 스택에서 데이터를 꺼내려 할 때 발생.
#             => pop 하기 전에 반드시 비어있는지 확인해야 한다.

print('=== Underflow 확인 ===')
empty_stack = []
try:
    empty_stack.pop()
except IndexError as e:
    print(f'  확인 없이 pop() 하면: IndexError - {e}')
print('  => 그래서 pop 함수 안에 비어있는지 검사하는 if 가 필요하다.')


print('\n' + '=' * 55 + '\n')


# ------------------------------------------------------------
# [스스로 점검하기]
# ------------------------------------------------------------
# Q1. peek 자리에 실수로 pop 을 쓰면 무슨 일이 벌어질까?
#
# Q2. stack[0] 은 스택의 무엇일까? top 일까, 바닥일까?
#
# Q3. append()/pop() 대신 insert(0, x)/pop(0) 으로 만들어도 동작은 한다.
#     그런데 왜 그렇게 쓰면 안 될까? (힌트: 앞에 끼워 넣으면 뒤 요소들은?)
#
# Q4. is_empty 를 if len(stack) == 0: return True / else: return False 로
#     쓸 수도 있다. 한 줄로 줄일 수 있는 이유는?
#
# Q5. push 함수 안에 stack = [] 를 넣으면 왜 아무것도 쌓이지 않을까?
