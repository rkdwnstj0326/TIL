from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    [커스텀 User 모델]
    - AbstractUser : Django 기본 User의 필드/기능(username, password 등)을 그대로 상속
    - 지금은 추가할 필드가 없어 pass 이지만, 나중을 위해 '내 User 모델'로 미리 교체해 둠
      => 프로젝트 중간에 User 모델을 바꾸는 것은 매우 어려움 (Django 공식 권장 사항)

    [필수 설정] settings.py
    - AUTH_USER_MODEL = 'accounts.User'
    - 반드시 첫 migrate 전에 설정해야 함
    """
    pass
    
