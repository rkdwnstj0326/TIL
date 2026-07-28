# =============================================================
# 메서드 오버라이딩 (Method Overriding)
# - 부모에게 물려받은 메서드를 자식이 '자기 방식으로 다시 정의'
# - 이름은 같지만 자식 버전이 부모 버전을 가림(재정의)
# - 용도: 공통 기능은 물려받되, 자식만의 동작이 필요할 때
# =============================================================


class Animal:
    def eat(self):
        print('Animal이 먹는 중')


class Dog(Animal):
    # 오버라이딩 (부모 클래스 Animal의 eat 메서드를 재정의)
    # => Dog 인스턴스로 eat()을 부르면 부모 것이 아닌 이 버전이 실행됨
    pass


my_dog = Dog()

my_dog.eat()  # Dog가 먹는 중   (부모의 'Animal이 먹는 중'이 아님)


# =============================================================
# [비교] 오버로딩(Overloading) - 파이썬은 지원하지 않음
# - 오버로딩: 이름이 같고 '매개변수 개수/형태가 다른' 메서드를
#             여러 개 두는 기능 (일부 다른 언어에는 있음)
# - 파이썬에서는 같은 이름이면 나중 정의가 앞을 '덮어써' 버림
#   => 아래 do_something은 결국 (self, x, y) 버전만 남음
#
# [실행 주의] 마지막 줄은 인자를 1개만 넘겨 TypeError가 발생함
#    남아 있는 do_something이 인자 2개(x, y)를 요구하기 때문
#    => 확인 후 주석 처리할 것
# =============================================================


# 오버로딩 (파이썬 미지원)
class Example:
    def do_something(self, x):
        print('첫 번째 do_something 메서드:', x)

    # 파이썬에서는 메서드가 "이름"이 같으면 앞선 정의를 덮어써버림
    def do_something(self, x, y):
        print('두 번째 do_something 메서드:', x, y)


example = Example()
# TypeError: Example.do_something() missing 1 required positional argument: 'y'
example.do_something(10)
