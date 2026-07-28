# =============================================================
# super() in 다중 상속 - "직계 부모"가 아니라 "MRO상 다음 순서"
# - 단일 상속에서 super()는 그냥 부모를 가리켰음
# - 하지만 다중 상속에서는 super()가 MRO(탐색 순서)를 따라
#   '현재 클래스의 다음 클래스'를 가리킴 (직계 부모가 아님)
# - 이 파일은 그 미묘한 동작을 실험으로 보여줌
# =============================================================


# 다중 상속
class ParentA:
    def __init__(self):
        # super().__init__()   <- 이 줄이 주석 처리된 것이 이 예제의 핵심
        self.value_a = 'ParentA'

    def show_value(self):
        print(f'Value from ParentA: {self.value_a}')


class ParentB:
    def __init__(self):
        self.value_b = 'ParentB'

    def show_value(self):
        print(f'Value from ParentB: {self.value_b}')


class Child(ParentA, ParentB):
    def __init__(self):
        super().__init__()  # ParentA 클래스의 __init__ 메서드 호출
        self.value_c = 'Child'

    def show_value(self):
        super().show_value()  # ParentA 클래스의 show_value 메서드 호출
        print(f'Value from Child: {self.value_c}')


# =============================================================
# 실행 흐름
# - Child()의 super().__init__() => MRO상 다음인 ParentA.__init__ 실행
# - 그런데 ParentA의 __init__ 안 super() 줄이 '주석 처리'되어 있어
#   여기서 연결이 끊김 => ParentB.__init__은 호출되지 않음
#   => 그 결과 value_b는 아예 만들어지지 않음
# =============================================================

child = Child()
child.show_value()
"""
Value from ParentA: ParentA
Value from Child: Child
"""

# =============================================================
# 속성 확인
# - value_c, value_a는 정상 => 각각 Child, ParentA에서 설정됨
# - value_b는 없음 => ParentB.__init__이 호출되지 않았기 때문
#
# [실행 주의] 마지막 print(child.value_b)는 AttributeError 발생
#    => 확인 후 주석 처리할 것
# =============================================================

print(child.value_c)  # Child
print(child.value_a)  # ParentA
print(
    child.value_b
)  # AttributeError: 'Child' object has no attribute 'value_b'


# =============================================================
# 아래 설명 블록들은 이 실험의 결론을 정리한 것 (실행되지 않는 문자열)
# =============================================================

"""
<ParentA에 super().__init__()를 주석 해제하면?>
그 다음으로 ParentB의 __init__가 실행되어 value_b도 초기화할 수 있음
그러면 print(child.value_b)는 ParentB를 출력하게 됨

print(child.value_b)  # ParentB
"""

"""
<Child 클래스의 MRO>
Child -> ParentA -> ParentB

super()는 단순히 “직계 부모 클래스를 가리킨다”가 아니라, 
MRO 순서를 기반으로 “현재 클래스의 다음 순서” 클래스(또는 메서드)를 가리킴

따라서 ParentA에서 super()를 부르면 MRO상 다음 클래스인 ParentB.__init__()가 호출됨
"""


"""
1.1 Child 클래스의 인스턴스를 생성할 때 일어나는 일
    1.	child = Child() 호출 시, Child.__init__()가 실행
    2.	Child.__init__() 내부에서 super().__init__()를 호출
        - 여기서 Child의 super()는 MRO에 의해 ParentA의 __init__()를 가리킴
    3.	ParentA.__init__()로 진입

1.2. ParentA.__init__() 내부
	1.	ParentA.__init__()에는 다시 super().__init__()가 있음
	2.	ParentA를 기준으로 MRO에서 “다음 클래스”는 ParentB, 따라서 ParentA의 super().__init__()는 ParentB.__init__() 호출
    3.	ParentB.__init__()가 실행되면서 self.value_b = 'ParentB'가 설정됨
	4.	ParentB.__init__()가 종료된 후, 다시 ParentA.__init__()로 돌아와 self.value_a = 'ParentA'가 설정됨
	5.	ParentA.__init__() 종료 후, 다시 Child.__init__()로 돌아감
	6.	마지막으로 Child.__init__() 내에서 self.value_c = 'Child'가 설정되고 종료

1.3 결과적으로 child 인스턴스는 value_a, value_b, value_c 세 속성을 모두 갖게 됨
	- child.value_a → 'ParentA'
	- child.value_b → 'ParentB' 
	- child.value_c → 'Child'
"""
