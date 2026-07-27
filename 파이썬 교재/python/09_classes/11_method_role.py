# =============================================================
# 메서드의 역할 - '할 수 있다(Can)' vs '해야 한다(Should)'
# - 기술적으로는 클래스도 인스턴스도 세 종류 메서드를 모두 호출 가능
# - 하지만 '가능하다'와 '그렇게 쓰는 게 좋다'는 다른 이야기
# - 각 메서드는 본래 의도된 호출 주체가 있음
# =============================================================

class MyClass:
    def instance_method(self):
        return 'instance method', self  # self: 호출한 인스턴스

    @classmethod
    def class_method(cls):
        return 'class method', cls  # cls: 클래스 자신

    @staticmethod
    def static_method():
        return 'static method'  # 받는 것 없음


instance = MyClass()

# =============================================================
# [1] 기술적 가능 여부 - 클래스도 사실 모두 호출할 수 있다
# - 단, instance_method는 self가 필요하므로 인스턴스를 직접 넘겨야 함
#   => MyClass.instance_method(instance)
# =============================================================

# 클래스가 할 수 있는 것
# 사실 클래스는 모든 메서드를 호출할 수 있음
print(MyClass.instance_method(instance))
print(MyClass.class_method())
print(MyClass.static_method())


# =============================================================
# [2] 인스턴스도 마찬가지로 모두 호출 가능
# - instance.class_method()도 되고 static_method()도 됨
#   (파이썬이 알아서 클래스를 찾아 처리)
# =============================================================

# 인스턴스가 할 수 있는 것
# 사실 인스턴스는 모든 메서드를 호출할 수 있음
print(instance.instance_method())
print(instance.class_method())
print(instance.static_method())


# =============================================================
# [3] 그렇다면 어떻게 써야 하는가 (Should)
# - '가능'하다고 아무렇게나 쓰면 코드의 의도가 흐려짐
# - 권장되는 사용 주체
#     클래스 메서드 / 정적 메서드 => 클래스가 호출
#     인스턴스 메서드            => 인스턴스가 호출
#   => 읽는 사람이 "이건 무엇에 대한 동작인지"를 바로 알 수 있게 됨
# =============================================================

# 기술적인 '가능 여부(Can)'와 논리적인 '사용 의도(Should)'를 구분해야 함
# 1. 클래스의 입장
# - 클래스 메서드와 정적 메서드를 호출하는 것이 주된 역할
print(MyClass.class_method())
print(MyClass.static_method())

# 2. 인스턴스의 입장
# - 인스턴스 메서드는 오직 인스턴스만 호출하는 것이 좋음
print(instance.instance_method())
