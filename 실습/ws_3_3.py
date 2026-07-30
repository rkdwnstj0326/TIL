#대여점에 있는 책 개수 : 100
# 홍길동이라는 사람이 책을 3권 빌리면 2가지를 해야한다
# 1. 보유중인 책을 97권으로 줄이고
# 2. 홍길동이 책 3권을 빌렸다는 문장을 출력

#책을 빌리는 전체 과정
#이 함수는 두가지 값을 받아야 함 - 1. 대여자의 이름, 2. 대여하는 책의 수 (매개변수 2개)
def rental_book(name,number):
    #왜 rental_book에서 decrease_book을 호출하는가
    decrease_book(number)

    print(f"{name}님이 {number}권의 책을 대여하였습니다.")

number_of_book = 100 
# number_of_book -> 상자 이름 / 100 -> 상자 안의 값

#책의 수를 줄이는 작업
def decrease_book(number): #함수 정의 -> decrease_book이라는 이름의 함수를 만들고 실행할 때 책의 수를 하나 전달 받을게~
    global number_of_book
    #global 쓰는 이유 : 내가 지금 사용하는 number_of_book은 함수 안에서 새로 만든 변수가 아니라, 
    #함수 밖에 있는 변수라는 걸 알려주기 위해서
    number_of_book = number_of_book - number
    print(f'남은 책의 수: {number_of_book}')

rental_book('홍길동',3)
