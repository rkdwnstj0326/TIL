# 1. 절댓값을 반환하는 함수 abs를 사용하여 아래 변수에 담긴 값의 절댓값을 출력하시오.
negative = -3

print(abs(negative))


# 2. 아래 변수에 담긴 값의 boolean 값을 출력하시오.
#boolean값 : 참인지 거짓인지 나타내는 값
empty_list = [3>5]
print(empty_list)


# 3. 주어진 리스트가 가진 모든 값을 더한 결과를 출력하시오.
my_list = [1, 2, 3, 4, 5]

print(sum(my_list))


# 4. 주어진 정렬을 오름차순으로 정렬한 결과를 출력하시오.
unsorted_list = ['하', '교', '캅', '의', '지', '가']

#오름차순 : sort() 아니면 sorted()
#리스트.sort -> 원래 리스트 자체를 정렬
#sorted(리스트) -> 정렬된 새 리스트를 만들어 반환

unsorted_list.sort()
print(sorted(unsorted_list))