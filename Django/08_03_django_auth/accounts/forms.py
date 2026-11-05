from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# ============================================================
# STEP 1. User 모델을 직접 import 하는 방식
# ============================================================
# from .models import User
#
#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User


# ============================================================
# STEP 2. 완성본 - get_user_model() 사용
# ============================================================
# [왜 User를 직접 import 하지 않을까?]
# - get_user_model() : settings.py의 AUTH_USER_MODEL에 지정된 User 모델을 반환
# - 나중에 User 모델이 바뀌어도 이 코드는 고칠 필요가 없음


class CustomUserCreationForm(UserCreationForm):
    """
    [회원가입 form]
    - Django 기본 UserCreationForm은 기본 User 모델에 연결되어 있음
    - 우리가 만든 커스텀 User 모델에 연결되도록 model만 교체
    """

    # 부모의 Meta를 상속 => 기존 설정(fields 등)은 그대로 두고 model만 덮어쓰기
    class Meta(UserCreationForm.Meta):
        model = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    """
    [회원 정보 수정 form]
    - 커스텀 User 모델에 연결 + 사용자가 수정할 수 있는 필드만 제한
    """

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        # 수정 가능한 필드를 반드시 직접 지정
        # => 지정하지 않으면 is_superuser, is_staff 같은 '권한' 필드까지 form에 노출되어
        #    일반 사용자가 스스로 관리자 권한을 줄 수 있음
        fields = ('first_name', 'last_name', 'email')
