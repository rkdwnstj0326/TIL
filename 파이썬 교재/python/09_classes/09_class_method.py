# =============================================================
# 클래스 메서드 (Class Method)
# - 특정 인스턴스가 아니라 '클래스 전체'와 관련된 일을 하는 메서드
# - @classmethod 데코레이터를 붙이고, 첫 인자는 cls (클래스 자신)
# - self가 '인스턴스'를 가리켰다면, cls는 '클래스'를 가리킴
# - 주 용도: 클래스 변수를 읽거나 바꾸는 작업
# =============================================================

class Person:
    population = 0  # 클래스 변수 (전체 인구 수, 모든 인스턴스 공유)

    def __init__(self, name):
        self.name = name
        # 인스턴스가 하나 생길 때마다 전체 인구를 1 증가시킴
        # => 개별 인스턴스가 아닌 '클래스 전체'의 상태를 바꾸는 일이므로
        #    클래스 메서드를 호출
        Person.increase_population()

    # 클래스 메서드
    @classmethod
    def increase_population(cls):
        # cls.population 은 Person.population 과 같음
        # (cls 자리에 Person이 자동으로 들어옴)
        cls.population += 1


# =============================================================
# 인스턴스를 2개 생성 => 생성될 때마다 __init__ 안에서
# increase_population()이 불려 population이 0 => 1 => 2
# =============================================================

# 인스턴스 생성
person1 = Person('Alice')
person2 = Person('Bob')

# 클래스 변수 접근
print(Person.population)  # 2
