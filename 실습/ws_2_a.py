# 아래에 코드를 작성하시오.
# zero_list 변수에 숫자 0을 하나 가지고 있는 리스트 할당
zero_list = [0]

# zero_list 변수 출력
print(zero_list)

#many_zero_list에 숫자 0을 25만개 가지고 있는 리스트
many_zero_list = [0] * 250000

# len을 활용해서 0의 개수를 나타냄
print(len(many_zero_list))

#numbers 변수에 range를 활용하여 1부터 10까지의 수를 가진 리스트를 할당
numbers = list(range(1,11))
print(numbers)

#numbers의 3번째 부터 마지막 요소까지 출력
print(numbers[3: ])