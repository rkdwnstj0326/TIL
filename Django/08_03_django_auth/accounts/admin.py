from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.
# 이제 우리는 기본 User클래스가 아니라 커스텀 User 클래스로
# 대체했기 때문에 admin에 새롭게 등록해줄 필요가 있음
admin.site.register(User, UserAdmin)
