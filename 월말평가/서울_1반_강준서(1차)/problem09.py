############## 주의 ##############
# 입력을 받기위한 input 함수는 절대 사용하지 않습니다.
# 별도 라이브러리 없이 구현합니다.

def manage_inventory(initial, commands):
    pass
    # 여기에 코드를 작성하여 함수를 완성합니다.

# 추가 테스트를 위한 코드 작성 가능
# 예) print(함수명(인자))

#####################################################
# 아래 코드를 삭제하는 경우 
# 모든 책임은 삭제한 본인에게 있습니다. 
############## 테스트 코드 삭제 금지 #################
# 처리 과정:
# 1) ('apple', -3): 재고 10 -> 출고 성공 -> apple = 7
# 2) ('banana', -8): 재고 5 < 8 -> 거부 (거부 1)
# 3) ('cherry', 4): 신규 입고 -> cherry = 4
# 4) ('apple', 5): 입고 -> apple = 12
# 5) ('banana', -2): 재고 5 >= 2 -> 출고 성공 -> banana = 3
initial = {'apple': 10, 'banana': 5}
commands = [('apple', -3), ('banana', -8), ('cherry', 4), ('apple', 5), ('banana', -2)]
print(manage_inventory(initial, commands))  # ({'apple': 12, 'banana': 3, 'cherry': 4}, 1)

print(manage_inventory({}, [('pen', -1), ('pen', 10), ('pen', -3)]))  # ({'pen': 7}, 1)
#####################################################
