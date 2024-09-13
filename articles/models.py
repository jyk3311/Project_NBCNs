from django.db import models
from django.conf import settings

"""
moels.Manager의 get_queryset 메소드를 호출하여 데이터를 조회할 때
is_authenticated가 True인 객체만을 조회하도록 
get_queryset 메소드를 오버라이딩함.
"""

# 삭제되지 않은 객체만 반환하는 커스텀 매니저
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_mine=True)


# Article과 Comment의 부모 클래스
class ArticleBaseModel(models.Model):
    # 장고에서 제공하는 기본 매니저를 커스텀 매니저로 사용
    objects = ActiveManager()

    '''
    ERRORS: articles.Comment.article: 
    (models.E006) The field 'article' clashes with the field 'article' from model 'articles.articlebasemodel'.
    실제로 부모 클래스에 article 필드가 존재하지 않지만 Comment.article 필드와 충돌이 생김
    Django는 ArticleBaseModel이 상속되는 과정에서
    부모 클래스에 article이라는 속성(메소드, 필드 등)이 있을 가능성을 먼저 확인하고
    그 결과 이름 충돌이 발생한다고 판단할 수 있다.
    '''
    class Meta:
        abstract = True  # 이 모델이 추상 클래스임을 지정

    def soft_delete(self):
        self.is_mine = False
        self.save()


class Article(ArticleBaseModel):
    category_choices = [("Free", "자유 게시판"),
                        ("Ask", "질문 게시판"), ("Company", "홍보 게시판")]
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=7, choices=category_choices)
    is_mine = models.BooleanField(default=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Comment(ArticleBaseModel):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)  # 댓글을 작성한 사용자를 참조
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')  # 댓글이 달린 기사를 참조
    is_mine = models.BooleanField(default=True)  # 댓글을 작성한 사용자가 인증된 사용자임을 나타냄
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
