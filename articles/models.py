from django.db import models
from django.conf import settings


class Article(models.Model):
    category_choices = [("Free", "자유 게시판"), ("Ask", "질문 게시판")]

    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=4, choices=category_choices)
    is_authenticated = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# Comment Model
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 댓글을 작성한 사용자를 참조
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # 댓글이 달린 기사를 참조
    is_mine = models.BooleanField(default=True)  # 댓글을 작성한 사용자가 인증된 사용자임을 나타냄
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
