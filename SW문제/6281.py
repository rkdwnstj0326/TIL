number = int(input())


# for n in range(1, 1 + number):
#     if number % n == 0 :
#         print(n)

# #리스트내포 만드는 법
# 표현식 for 항목 in 반복가능한 객체 if 조건식

result = [n for n in range(1, 1 + number) if number % n == 0]
print(result)