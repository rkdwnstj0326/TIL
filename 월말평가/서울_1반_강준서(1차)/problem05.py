############## 주의 ##############
# 입력을 받기위한 input 함수는 절대 사용하지 않습니다.
# 제한 내장 함수: sum, len, map
# 기본 점수 (9점): 제한 내장 함수를 사용하여 해결
# 가산점(+3점): 제한 내장 함수 없이 직접 구현 (총 12점)

def count_items(inventory):
    count = 0

    for bag in inventory: #inventory에서 bag를 꺼냄. 그럼 [101,0,205]가 나옴
        for item in bag: #bag에서 item을 꺼냄 -> 그럼 101, 0 205 를 꺼냄
            if item: # item이 있다면~~ 즉 0 이 아닌 숫자가 있다면
                count = count + 1 # 갯수를 누적하라
    return count

    # return str(map(len, inventory))
    # result = 0
    # j=0

    # for i in inventory:
    #     for j in i:
    #         return len([i][j])
        

# 추가 테스트를 위한 코드 작성 가능
# 예) print(함수명(인자))

#####################################################
# 아래 코드를 삭제하는 경우 
# 모든 책임은 삭제한 본인에게 있습니다. 
############## 테스트 코드 삭제 금지 #################
print(count_items([[101, 0, 205], [33, 4, 5], [0]]))  # 5
print(count_items([[0, 0], [0], [88, 90]]))           # 2
#####################################################
