# 아래 함수를 수정하시오.
def check_number():
    try:
        num = int(input('숫자를 입력하세요: ')) #입력받은 문자열을 정수로 변환한다.

    except ValueError:
        print('잘못된 입력입니다.') #숫자로 변환할 수 없는 값을 입력한 경우

    else: # 오류가 발생하지 않았을 경우
        if num > 0:
            print('양수입니다.')

        elif num == 0:
            print('0입니다.')

        else:
            print('음수입니다.')
        

check_number()
