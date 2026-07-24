# =============================================================
# 딕셔너리 메서드
# - 딕셔너리는 '키(key)'로 '값(value)'을 찾는 자료구조
# - 리스트가 위치(인덱스)로 찾는다면, 딕셔너리는 이름표로 찾음
# - 키는 중복 불가 / 값은 중복 가능
# =============================================================

# =============================================================
# [1] get - 키가 없어도 에러 없이 안전하게 조회
# - person['country']는 키가 없으면 KeyError로 프로그램이 멈춤
# - get은 없으면 None을 반환하고, 두 번째 인자로 기본값 지정 가능
#   => 사용자 입력처럼 키가 있을지 확신할 수 없을 때 유용
# =============================================================

# get
person = {'name': 'Alice', 'age': 25}
print(person.get('name'))
print(person.get('country'))
print(person.get('country', 'Unknown'))
# print(person['country'])  # KeyError: 'country'

# =============================================================
# [2] keys / values / items - 순회를 위한 3형제
# - keys()   : 키만 모아서 반환
# - values() : 값만 모아서 반환
# - items()  : (키, 값) 쌍을 튜플로 묶어 반환
# - 반환값은 리스트가 아니라 dict_keys 같은 '뷰(view)' 객체
#   => 인덱스 접근(keys()[0])은 불가, 반복문 순회는 가능
# =============================================================

# keys
person = {'name': 'Alice', 'age': 25}
print(person.keys())  # dict_keys(['name', 'age'])
for item in person.keys():
    print(item)

# values
person = {'name': 'Alice', 'age': 25}
print(person.values())  # dict_values(['Alice', 25])
for item in person.values():
    print(item)

# -------------------------------------------------------------
# items()는 튜플을 반환하므로 for key, value 형태로 언패킹해 받음
# => 키와 값을 동시에 써야 할 때 가장 많이 쓰는 방식
# -------------------------------------------------------------

# items
person = {'name': 'Alice', 'age': 25}
print(person.items())  # dict_items([('name', 'Alice'), ('age', 25)])
for key, value in person.items():
    print(key, value)


# =============================================================
# [3] setdefault - 조회하되, 없으면 만들어 넣기
# - 키가 있으면 그 값을 반환 (아무것도 바꾸지 않음)
# - 키가 없으면 기본값으로 '추가한 뒤' 그 값을 반환
#   => get과 달리 딕셔너리 자체가 변한다는 점이 핵심 차이
# =============================================================

# setdefault
person = {'name': 'Alice', 'age': 25}
print(person.setdefault('country', 'KOREA'))  # KOREA
print(person)  # {'name': 'Alice', 'age': 25, 'country': 'KOREA'}

# =============================================================
# [4] update - 다른 딕셔너리의 내용으로 갱신
# - 같은 키가 있으면 '덮어쓰고', 없는 키는 '새로 추가'
#   => name은 Alice에서 Jane으로 덮어써지고, country는 추가됨
# - 키워드 인자 형태(age=100)로도 전달 가능
# =============================================================

# update
person = {'name': 'Alice', 'age': 25}
other_person = {'name': 'Jane', 'country': 'KOREA'}

person.update(other_person)
print(person)  # {'name': 'Jane', 'age': 25, 'country': 'KOREA'}

person.update(age=100, address='SEOUL')
print(
    person
)  # {'name': 'Jane', 'age': 100, 'country': 'KOREA', 'address': 'SEOUL'}

# =============================================================
# [5] pop - 키를 제거하면서 그 값을 반환
# - 리스트의 pop은 '위치'로, 딕셔너리의 pop은 '키'로 꺼냄
# - 없는 키를 꺼내면 KeyError => 두 번째 인자로 기본값을 주면 안전
# =============================================================

# pop
person = {'name': 'Alice', 'age': 25}
print(person.pop('age'))  # 25
print(person)  # {'name': 'Alice'}
print(person.pop('country', None))  # None
# print(person.pop('country'))  # KeyError: 'country'

# =============================================================
# [6] clear - 모든 키/값 쌍을 제거 (빈 딕셔너리가 됨)
# =============================================================

# clear
person = {'name': 'Alice', 'age': 25}
person.clear()
print(person)  # {}
