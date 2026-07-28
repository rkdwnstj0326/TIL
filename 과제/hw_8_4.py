# 단순하게 이름이랑 나이를 입력받는 것이 아니라, 입력 결과에 따라 true, false, none 을 다르게 반환하는 것이 핵심임

class UserInfo: # userinfo 객체 만들기 / userinfo라는 클래스 만들기     
    def __init__(self): #__init__은 객체가 만들어질 때 자동으로 실행되는 생성자 메서드 
        self.user_data = {} #self : 현재 만들어진 객체 자신을 의미. user객체를 가리킴

    def get_user_info(self):
        """
        사용자로부터 이름과 나이를 입력받습니다.
        - 이름이 없거나 공백이면 None을 반환합니다.
        - 나이가 숫자가 아니거나 입력되지 않으면 ValueError를 처리하고 False를 반환합니다.
        - 올바르게 입력되면 사용자 정보를 저장하고 True를 반환합니다.
        """
        # TODO: 아래 코드를 문제 요구사항에 맞게 완성하세요.
        name = input('이름을 입력하세요: ')

        if not name.strip():
            return None

        try:
            age = int(input('나이를 입력하세요: '))

        except ValueError:
            print('나이는 숫자로 입력해야 합니다.')
            return False

        self.user_data['이름'] = name
        self.user_data['나이'] = age

        return True

    def display_user_info(self): 
        """
        저장된 사용자 정보를 출력합니다.
        - 정보가 없으면 "사용자 정보가 입력되지 않았습니다."를 출력합니다.
        """
        # TODO: 아래 코드를 문제 요구사항에 맞게 완성하세요.
        if not self.user_data:
            print('사용자 정보가 입력되지 않았습니다.')

        else:
            print('사용자 정보: ')
            print(f"이름: {self.user_data['이름']}")
            print(f"나이: {self.user_data['나이']}")


# 아래 코드는 수정하지 마세요.
user = UserInfo()
result = user.get_user_info()

if result is True:
    user.display_user_info()
elif result is None:
    # 이름이 입력되지 않은 경우, display_user_info()가 적절한 메시지를 출력해야 합니다.
    user.display_user_info()
# 나이가 잘못 입력된 경우 (result is False), get_user_info()에서 이미 메시지를 출력했으므로
# 추가적인 동작이 필요 없습니다.


