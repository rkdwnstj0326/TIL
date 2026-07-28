# =============================================================
# 상속은 '왜' 필요한가 - 중복 제거
# - 상속이 없으면 여러 클래스에 같은 코드를 반복해서 써야 함
# - 공통 부분을 부모로 올리면, 자식들은 그것을 물려받아 재사용
#
# [실행 주의] 이 파일은 학습을 위해 같은 이름의 클래스
#    (Person, Professor, Student)를 여러 번 재정의합니다.
#    파이썬은 나중 정의가 앞을 덮어쓰므로, 실제로 동작하는 것은
#    '마지막에 정의된 상속 버전'입니다. 위쪽 예시는 개념 비교용입니다.
# =============================================================

# =============================================================
# [1] 상속이 필요한 상황 - 우선 Person 하나만 있을 때
# =============================================================


# 상속 없는 경우 - 1
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def talk(self):
        print(f'반갑습니다. {self.name}입니다.')


s1 = Person('김학생', 23)
s1.talk()  # 반갑습니다. 김학생입니다.

p1 = Person('박교수', 59)
p1.talk()  # 반갑습니다. 박교수입니다.


# =============================================================
# [2] 상속이 없다면 - 같은 코드가 계속 중복됨
# - Professor와 Student 모두 name, age, talk를 각자 다시 작성
#   => talk 메서드가 그대로 복사됨 (중복)
#   => 나중에 talk를 고치려면 모든 클래스를 일일이 수정해야 함
# =============================================================


# 상속 없는 경우 - 2
class Professor:
    def __init__(self, name, age, department):
        self.name = name
        self.age = age
        self.department = department

    def talk(self):  # 중복
        print(f'반갑습니다. {self.name}입니다.')


class Student:
    def __init__(self, name, age, gpa):
        self.name = name
        self.age = age
        self.gpa = gpa

    def talk(self):  # 중복
        print(f'반갑습니다. {self.name}입니다.')


# =============================================================
# [3] 상속으로 해결 - 공통 부분을 부모(Person)로 올림
# - Professor와 Student는 Person을 상속받아 talk를 물려받음
#   => 자식에는 talk를 다시 쓰지 않아도 됨 (중복 제거)
# - talk를 수정할 일이 생겨도 Person 한 곳만 고치면 전부 반영됨
#
# 참고: 자식의 __init__에서 name, age를 반복하고 있는데,
#    이 중복마저 없애는 방법이 다음에 배울 super() (05번 파일)
# =============================================================


# 상속을 사용한 계층구조 변경
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def talk(self):  # 메서드 재사용
        print(f'반갑습니다. {self.name}입니다.')


class Professor(Person):
    def __init__(self, name, age, department):
        self.name = name
        self.age = age
        self.department = department


class Student(Person):
    def __init__(self, name, age, gpa):
        self.name = name
        self.age = age
        self.gpa = gpa


p1 = Professor('박교수', 49, '컴퓨터공학과')
s1 = Student('김학생', 20, 3.5)

# 부모 Person 클래스의 talk 메서드를 활용
p1.talk()  # 반갑습니다. 박교수입니다.

# 부모 Person 클래스의 talk 메서드를 활용
s1.talk()  # 반갑습니다. 김학생입니다.
