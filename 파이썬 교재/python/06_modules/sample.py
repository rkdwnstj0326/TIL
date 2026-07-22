import my_math

# from my_math import add

print(my_math.add(1, 2))
# print(add(1, 2))


# 직접 만든 패키지 사용하기
from my_package.math import my_math
from my_package.statistics import tools

print(my_math.add(1, 2))  # 3
print(tools.mod(1, 2))  # 1
