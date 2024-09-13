from django.db import models
from django.conf import settings  # User 모델이 AUTH_USER_MODEL로 설정되어 있을 때 이를 사용

# NBCN 모델


class NBCN(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=500)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    nbcn_bookmark_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='bookmark_nbcns')

    def __str__(self):
        return self.title

