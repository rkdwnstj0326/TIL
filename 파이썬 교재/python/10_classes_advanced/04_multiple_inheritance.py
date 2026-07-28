# =============================================================
# 다중 상속 (Multiple Inheritance)
# - 하나의 자식이 '여러 부모'를 동시에 상속받는 것
# - 문법: class 자식(부모1, 부모2):
# - 여러 부모의 기능을 한 번에 물려받을 수 있지만,
#   같은 이름의 속성/메서드가 겹치면 '순서'가 중요해짐
# =============================================================


# 다중 상속 예시
class Person:
    def __init__(self, name):
        self.name = name

    def greeting(self):
        return f'안녕, {self.name}'


class Mom(Person):
    gene = 'XX'

    def swim(self):
        return '엄마가 수영'


class Dad(Person):
    gene = 'XY'

    def walk(self):
        return '아빠가 걷기'


# =============================================================
# FirstChild(Dad, Mom) - Dad와 Mom을 함께 상속
# - swim은 자신이 재정의(오버라이딩)했으므로 자기 것을 사용
# - walk는 Dad에게서, greeting은 Person에게서 물려받음
# =============================================================


class FirstChild(None):
    def swim(self):
        return '첫째가 수영'

    def cry(self):
        return '첫째가 응애'


baby1 = FirstChild('아가')
print(baby1.cry())  # 첫째가 응애    (자신의 메서드)
print(baby1.swim())  # 첫째가 수영   (오버라이딩한 자신의 메서드)
print(baby1.walk())  # 아빠가 걷기   (Dad에게 물려받음)

# =============================================================
# [핵심 질문] baby1.gene은 XX일까 XY일까?
# - Mom도 gene='XX', Dad도 gene='XY'를 가지고 있어 이름이 충돌
# - 파이썬은 상속 순서(Dad, Mom)를 기준으로 '먼저 쓴 쪽'을 우선함
#   => class FirstChild(Dad, Mom) 에서 Dad가 앞이므로 XY
# - 이 탐색 순서를 MRO(Method Resolution Order)라고 함
#   (자세한 내용은 99_mro.py에서 학습)
# =============================================================

# print(baby1.gene)  # ??
