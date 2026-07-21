# =============================================================
# 스코프 (Scope) - 변수가 유효한 범위
#
# ⚠️ [실행 주의] 이 파일에는 의도적인 에러가 2곳 있습니다.
#    - [1]번의 NameError, [2]번의 TypeError
#    => 실행 시 해당 지점에서 멈추므로,
#       확인 후 주석 처리하고 다음 구역을 이어서 실행할 것
# =============================================================

# =============================================================
# [1] 지역 스코프 (Local Scope)
# - 함수 안에서 만든 변수는 그 함수 안에서만 존재
# - 함수가 끝나면 사라지므로 바깥에서는 접근 불가 => NameError
# =============================================================

# Scope 예시
def func():
    num = 20
    print('local', num)  # local 20


func()

print('global', num)  # NameError: name 'num' is not defined


# =============================================================
# [2] 내장(Built-in) 이름을 덮어쓰는 실수
# - sum은 원래 내장 함수인데, 변수명으로 써버리면 함수가 사라짐
# - 이후 sum(...)을 호출하면 '정수를 호출하려 한다'는 TypeError
# - 실무에서도 자주 나오는 실수: list, str, id, type, max 등에 주의
# =============================================================

# 내장 함수 sum의 이름을 사용해버려서 오류가 발생하는 예시
print(sum)  # <built-in function sum>
print(sum(range(3)))  # 3
sum = 5
print(sum)  # 5
print(sum(range(3)))  # TypeError: 'int' object is not callable


# =============================================================
# [3] LEGB Rule 퀴즈
# - 파이썬이 이름을 찾는 순서
#   L(Local 지역) => E(Enclosing 감싸는 함수) => G(Global 전역) => B(Built-in 내장)
#
# [풀이 힌트]
#  inner_func(y) 의 y는 '매개변수' => Local
#  x는 inner_func 안에 없으므로 Enclosing(outer_func)의 'E'
#  안쪽에서 값을 바꾼 것이 아니므로 바깥 x, y는 그대로 유지됨
# =============================================================

# LEGB Rule 퀴즈
x = 'G'
y = 'G'


def outer_func():
    x = 'E'
    y = 'E'

    def inner_func(y):
        z = 'L'
        print(x, y, z)  # E P L

    inner_func('P')
    print(x, y)  # E E


outer_func()
print(x, y)  # G G
