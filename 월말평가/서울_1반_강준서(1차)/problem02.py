############## 주의 ##############
# 입력을 받기위한 input 함수는 절대 사용하지 않습니다.
# 제한 내장 함수:  len
# 기본 점수 (9점): 제한 내장 함수를 사용하여 해결
# 가산점(+3점): 제한 내장 함수 없이 직접 구현 (총 12점)

def count_long_names(names, min_length):
    for name in names:
        if len(name) >= int(min_length):
            return len(name)
        else:
            return '0'

    # 반복문을 활용해서 숫자보다 길이가 긴지 출력   

# 추가 테스트를 위한 코드 작성 가능
# 예) print(함수명(인자))

#####################################################
# 아래 코드를 삭제하는 경우 
# 모든 책임은 삭제한 본인에게 있습니다. 
############## 테스트 코드 삭제 금지 #################
print(count_long_names(['kim', 'developer', 'ssafy', 'a'], 5))  # 2 ('developer', 'ssafy')
print(count_long_names(['a', 'bb', 'ccc'], 5))                  # 0
#####################################################
