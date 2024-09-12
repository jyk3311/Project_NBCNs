from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_authenticated = models.BooleanField(default=False) #True면 master, False면 Newbie



    # 회원탈퇴 시, 계정을 비활성화 상태로 변경
    def soft_delete(self):
        self.is_active=False
        self.save()
