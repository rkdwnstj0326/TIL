# 아래 클래스를 수정하시오.
# 문자열을 원하는 횟수만큼 출력하는 기능을 클래스 안에 만든 것


class StringRepeater: #sringrepeater이라는 이름의 클래스를 만드는 코드

    def repeat_string(self, count, string): #repeat_string이라는 메서드를 정의
        # (self, count, string) : 메서드를 실행할 때 필요한 값을 받는 자리(매개변수)
        for _  in range(count):
            print(string)


repeater1 = StringRepeater()
repeater1.repeat_string(3, "Hello")

# # 일반함수로 코드 짜는 방법

# def repeat_string(count,string):
#     for _ in range(count):
#         print(string)

# repeat_string(3,"Hello")

