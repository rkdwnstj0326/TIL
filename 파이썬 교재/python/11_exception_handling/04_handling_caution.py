# =============================================================
# [주의] except 순서 - 구체적인 예외를 먼저 써야 한다
# - 예외들은 상속 관계(계층 구조)를 가짐
#   예) ZeroDivisionError, ValueError는 모두 Exception의 하위(자식)
# - except는 위에서부터 검사하며, '처음 맞는 것 하나'만 실행됨
#   => 부모(Exception)를 위에 두면, 자식들이 전부 거기서 걸려버림
#
# [실행 주의] 두 예제 모두 input()으로 입력을 기다립니다.
#    (첫 예제는 순서가 잘못되어 뒤쪽 except가 무의미해지는 예시)
#
# 참고: 파이썬 예외 계층 구조
# https://docs.python.org/ko/3/library/exceptions.html#exception-hierarchy
# =============================================================

# =============================================================
# [1] 잘못된 순서 - 범용 예외(Exception)를 맨 위에 둠
# - 모든 예외는 Exception의 자식이므로, 어떤 에러든 첫 except에서
#   전부 잡혀버림
#   => 아래의 ZeroDivisionError, except: 는 '절대 도달하지 못하는
#      죽은 코드'가 됨 (unreachable)
# - 문법 에러는 아니라서 조용히 잘못 동작하므로 더 위험함
# =============================================================

# 아래와 같이 예외를 작성하면 코드는 2번째 except 절에 이후로 도달하지 못함
# ZeroDivisionError 클래스는 Exception 클래스의 하위 클래스 중 하나이므로 ZeroDivisionError를 먼저 작성해야 함
try:
    num = int(input('100으로 나눌 값을 입력하시오 : '))
    print(100 / num)
except Exception:
    print('숫자를 넣어주세요.')
# ZeroDivisionError는 Exception의 하위 클래스이므로 Exception보다 먼저 작성해야 함
except ZeroDivisionError:
    print('0으로 나눌 수 없습니다.')
except:
    print('에러가 발생하였습니다.')


# =============================================================
# [2] 올바른 순서 - 구체적인 것부터, 범용적인 것을 마지막에
# - 좁은 그물(구체적 예외)을 먼저 치고, 넓은 그물(Exception)을 뒤에
#   ZeroDivisionError, ValueError => 각각 정확한 메시지로 처리
#   Exception                     => 위에서 못 잡은 나머지를 마지막에
# - 규칙: except는 항상 '구체적인 것 => 일반적인 것' 순서로 배치
# =============================================================

# 옳은 코드
# 가장 구체적인 예외부터 처리하고, 마지막에 범용 예외를 처리하도록 순서를 배치
try:
    num = int(input('100으로 나눌 값을 입력하시오 : '))
    print(100 / num)
# 1) 구체적인 예외부터
except ZeroDivisionError:
    print('0으로 나눌 수 없습니다.')
except ValueError:
    print('숫자를 넣어주세요.')
# 2) 마지막에 광범위한 예외(Exception)
except Exception:
    print('에러가 발생하였습니다.')
