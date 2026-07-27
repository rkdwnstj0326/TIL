# 문제
# 사람의 이름과 나이를 입력받아 자신을 소개하는 Person 클래스를 작성하시오.
# 클래스에는 자신을 소개하는 introduce 인스턴스 메서드가 포함되어야 하고, 
# 인스턴스가 생성될 때 마다 증가하는 number_of_people 클래스 변수가 작성되어야 한다.
# 아래 클래스를 수정하시오.

#1번 
# class Person:
#     number_of_people = 0
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age

#         Person.number_of_people += 1

#     def introduce(self):
#         print(f'제 이름은 {self.name}이고, 저는 {self.age}살 입니다.')


# person1 = Person("Alice", 25)
# person1.introduce()
# print(Person.number_of_people)

#2번
class Person:
    number_of_people = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age

        Person.increase_people()

    @classmethod
    def increase_people(cls):
        cls.number_of_people += 1

    def introduce(self):
        print(f'제 이름은 {self.name}이고, 저는 {self.age}살 입니다.')


person1 = Person("Alice", 25)
# person2 = Person("jaek",30)
person1.introduce()
print(Person.number_of_people)

# 1번이랑 2번이랑 차이가 무엇인가
# 차이 : 사람 수를 증가시키는 코드를 어디에 작성했는가
# 1번 : init안에서 직접 사람 수를 1 증가시킴
# 2번 : init안에서 사람 수를 직접 증가시키지 않고, 사람 수를 증가시키는 별도의 클래스 매서드를 호출

