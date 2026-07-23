# 아래 함수를 수정하시오.
def find_min_max(numbers):
    minimum = min(numbers) #최솟값 찾기
    maximum = max(numbers) #최댓값 찾기

    return(minimum, maximum)



result = find_min_max([3, 1, 7, 2, 5])
print(result)  # (1, 7)
