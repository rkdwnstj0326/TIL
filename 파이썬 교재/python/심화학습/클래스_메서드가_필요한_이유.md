[toc]

## 클래스 메서드가 필요한 이유: "상속과 클래스 단위 데이터 관리"

클래스 메서드는 **인스턴스에 종속되지 않고 클래스 자체의 데이터를 관리**할 때, 특히 **상속 관계**에서 매우 유용한 기능을 제공합니다.

이번 예제에서는 `Animal`이라는 부모 클래스와 이를 상속받는 `Dog`, `Cat` 자식 클래스를 통해 클래스 메서드가 왜 필요한지 알아보겠습니다.

### 1. 핵심 개념 요약

1.  **클래스 메서드의 장점**

      * 인스턴스를 만들지 않고도 클래스 속성(`total_count` 등)에 직접 접근하고 관리할 수 있습니다.
      * 자식 클래스가 부모 클래스의 클래스 메서드를 재사용하면서, 자신만의 로직(예: `dog_count` 관리)을 추가하기 용이합니다.

2.  **`cls` 키워드의 의미**
      * 메서드가 호출된 **현재 클래스 자체**를 가리킵니다. (`self`가 인스턴스를 가리키는 것과 유사)
      * `Dog.get_dog_info()`에서 `cls`는 `Dog` 클래스를, `Cat.get_cat_info()`에서는 `Cat` 클래스를 가리킵니다.
    
3.  **상속과 클래스 메서드**
      * `cls` 덕분에 자식 클래스(`Dog`, `Cat`)는 부모의 클래스 메서드(`get_total_count`)를 마치 자신의 것처럼 호출할 수 있습니다.
      * 이를 통해 중복 코드를 줄이고, 클래스 단위의 데이터를 각 클래스에 맞게 유연하게 처리할 수 있습니다.



### 2. 예제 코드

```python
class Animal:
    total_count = 0  # 모든 동물의 총 개수 (클래스 속성)

    def __init__(self, name):
        self.name = name
        Animal.total_count += 1

    @classmethod
    def get_total_count(cls):
        """모든 동물의 수를 반환하는 클래스 메서드"""
        return f'전체 동물 수: {cls.total_count}'


class Dog(Animal):
    dog_count = 0  # Dog 클래스만의 강아지 개수

    def __init__(self, name, breed):
        super().__init__(name)  # 부모 클래스의 __init__ 호출
        self.breed = breed
        Dog.dog_count += 1

    @classmethod
    def get_dog_info(cls):
        """
        부모의 클래스 메서드와 자신의 클래스 속성을 함께 사용.
        cls는 Dog 클래스를 가리킨다.
        """
        return f'{cls.get_total_count()}, 강아지 수: {cls.dog_count}'


class Cat(Animal):
    cat_count = 0  # Cat 클래스만의 고양이 개수

    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
        Cat.cat_count += 1

    @classmethod
    def get_cat_info(cls):
        """
        부모의 클래스 메서드와 자신의 클래스 속성을 함께 사용.
        cls는 Cat 클래스를 가리킨다.
        """
        return f'{cls.get_total_count()}, 고양이 수: {cls.cat_count}'
```



### 3. 실행 및 결과

```python
# Dog 인스턴스 생성
dog1 = Dog('멍멍이', '삽살개')
dog2 = Dog('바둑이', '진돗개')

# Cat 인스턴스 생성
cat1 = Cat('노아', '페르시안')
cat2 = Cat('루비', '코숏')

# 각 클래스의 정보 확인
print(Dog.get_dog_info())
print(Cat.get_cat_info())
```

**출력 결과:**

```
전체 동물 수: 4, 강아지 수: 2
전체 동물 수: 4, 고양이 수: 2
```

`Dog.get_dog_info()` 메서드는 `cls`를 통해 부모인 `Animal`의 `get_total_count()`를 호출하여 전체 동물 수를 가져오고, 동시에 자신만의 클래스 속성인 `dog_count`에 접근하여 강아지 수를 함께 보여줍니다.

이처럼 클래스 메서드는 **클래스 레벨의 데이터를 관리**하거나, **상속 시 부모 메서드를 재사용**하여 코드의 효율성과 유지보수성을 높일 때 매우 유용합니다.