# 아래에 코드를 작성하시오.
# 요구사항
# Myth 클래스를 정의한다. 
# Myth의 인스턴스 수를 기록 할 수 있는 클래스 변수 type_of_myth를 정의하고, 0을 할당한다. 
# 생성자 메서드를 정의한다. 
# 생성자 메서드는 신화의 이름을 인자로 받는다. 
# 각 인스턴스는 고유한 이름을 담을 수 있는 name 변수를 가지고, 인자로 넘겨받은 이름을 할당 받는다. 
# 인스턴스가 생성될 때 마다 type_of_myth가 1 증가해야 한다. 

# `신화`에 대한 설명을 출력하는 description 스태틱 메서드를 정의한다. 

# 2개 이상의 인스턴스를 생성하고, 각 인스턴스의 name을 출력한다. 
# Myth 클래스의 type_of_myth를 출력한다. 
# description 스태틱 메서드를 호출한다.

class Myth:
    type_of_myth = 0

    def __init__(self,name) :
        self.name = name
        Myth.type_of_myth += 1

    @staticmethod
    def description():
        print('신화는 한 나라 혹은 한 민족으로부터 전승되어 오는 예로부터 섬기는 신을 둘러싼 이야기를 뜻한다.')

myth1 = Myth('dangun')
myth2 = Myth('greek & rome')

print(myth1.name)
print(myth2.name)
print(f'현재까지 생성된 신화 수 : {Myth.type_of_myth}')

Myth.description()
