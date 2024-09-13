from django.db import models
from django.conf import settings

"""
moels.Manager의 get_queryset 메소드를 호출하여 데이터를 조회할 때
is_authenticated가 True인 객체만을 조회하도록 
get_queryset 메소드를 오버라이딩함.
"""


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_mine=True)


class Article(models.Model):
    category_choices = [("Free", "자유 게시판"),
                        ("Ask", "질문 게시판"), ("Company", "홍보 게시판")]

    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=7, choices=category_choices)
    is_mine = models.BooleanField(default=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_articles'
    )

    bookmark_articles = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='bookmark_users'
    )

    # 장고에서 제공하는 기본 매니저를 커스텀 매니저로 사용
    objects = ArticleManager()

    def __str__(self):
        return self.title

    def soft_delete(self):
        self.is_mine = False
        self.save()
