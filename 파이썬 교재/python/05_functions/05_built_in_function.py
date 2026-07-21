# =============================================================
# 내장 함수 (Built-in Function)
# - 파이썬에 기본으로 포함되어 있어 별도 설치/import 없이 바로 사용
# - 자주 쓰는 것: len, max, min, sum, sorted, type, range, print ...
# - sorted()는 원본을 바꾸지 않고 '정렬된 새 리스트'를 반환
#   => reverse=True 처럼 이름을 지정해 전달하는 것이 키워드 인자
# =============================================================

numbers = [1, 2, 3, 4, 5]

print(numbers)  # [1, 2, 3, 4, 5]
print(len(numbers))  # 5
print(max(numbers))  # 5
print(min(numbers))  # 1
print(sum(numbers))  # 15
print(sorted(numbers, reverse=True))  # [5, 4, 3, 2, 1]
