# =============================================================
# super() - 부모 클래스에 접근하는 함수 (단일 상속)
# - 앞 파일들에서 자식의 __init__이 부모와 똑같은 코드를
#   반복하던 문제(name, age 재작성)를 해결
# - super()는 부모 클래스를 가리키므로, 부모의 __init__을 그대로
#   불러다 쓰면 중복을 없앨 수 있음
#
# 참고: super()는 클래스가 아니라 '함수처럼 호출'하는 것이고,
#       그 뒤의 .__init__()는 부모의 '메서드'
#
# 이 파일은 클래스 정의만 있고 실행/출력 코드는 없음 (구조 비교용)
# =============================================================

# 단일 상속


# =============================================================
# [1] super를 쓰지 않았을 때 - 부모 코드를 그대로 복사
# - Student가 name, age, number, email을 부모와 똑같이 다시 씀
#   => 부모 Person에 이미 있는 코드인데 중복됨
#   => Person의 초기화 방식이 바뀌면 Student도 따로 고쳐야 함
# =============================================================


# super를 사용하지 않았을 때
class Person:
    def __init__(self, name, age, number, email):
        self.name = name
        self.age = age
        self.number = number
        self.email = email


class Student(Person):
    def __init__(self, name, age, number, email, student_id):
        self.name = name
        self.age = age
        self.number = number
        self.email = email
        self.student_id = student_id


# =============================================================
# [2] super를 사용했을 때 - 부모의 초기화를 위임
# - super().__init__(...)로 Person의 __init__을 호출
#   => 공통 속성(name~email)은 부모가 처리하도록 맡김
# - 자식은 자기만의 속성(student_id)만 추가로 설정
#   => 중복이 사라지고, 부모가 바뀌면 자동으로 반영됨
# =============================================================


# super를 사용했을 때
class Person:
    def __init__(self, name, age, number, email):
        self.name = name
        self.age = age
        self.number = number
        self.email = email


class Student(Person):
    def __init__(self, name, age, number, email, student_id):
        # super()를 통해 Person의 __init__ 메서드 호출
        super().__init__(name, age, number, email)
        self.student_id = student_id
