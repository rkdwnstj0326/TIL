############## 주의 ##############
# 입력을 받기위한 input 함수는 절대 사용하지 않습니다.
# 아래 group_by_dept 함수에는 버그가 있습니다.
# 실행 결과가 왜 잘못 나오는지 원인을 파악하여 함수를 수정하시오.
# (단, 함수명은 수정 불가)
def group_by_dept(employees):
    result = {}
    names = []
    for e in employees:
        if e['dept'] not in result:
            result[e['dept']] = names
        result[e['dept']].append(e['name'])
    return result

# 추가 테스트를 위한 코드 작성 가능
# 예) print(함수명(인자))

#####################################################
# 아래 코드를 삭제하는 경우
# 모든 책임은 삭제한 본인에게 있습니다.
############## 테스트 코드 삭제 금지 #################
employees = [
    {'name': 'Kim', 'dept': 'Dev'},
    {'name': 'Lee', 'dept': 'Dev'},
    {'name': 'Park', 'dept': 'HR'},
    {'name': 'Choi', 'dept': 'Sales'}
]
# 기대결과:
# {
#   'Dev': ['Kim', 'Lee'],
#   'HR': ['Park'],
#   'Sales': ['Choi']
# }
print(group_by_dept(employees))
#####################################################
