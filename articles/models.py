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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
