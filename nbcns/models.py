from django.db import models
from django.conf import settings  # User 모델이 AUTH_USER_MODEL로 설정되어 있을 때 이를 사용

# NBCN 모델
class NBCN(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=500)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# NBCN 북마크 모델
class NBCN_Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    NBCN = models.ForeignKey(NBCN, on_delete=models.CASCADE)  # NBCN 모델 클래스와 일치하도록 대소문자 맞춤

    def __str__(self):
        return f'{self.user.username} bookmarked {self.NBCN.title}'