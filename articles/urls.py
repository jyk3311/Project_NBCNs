from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListCreateAPIView.as_view()),
    path("<str:category>/", views.CategoryArticleListAPIView.as_view()),
    path("<int:pk>", views.ArticleDetailAPIView.as_view()),# GET(댓글 조회) & POST(댓글 작성)
    path('<int:pk>/comments/', views.CommentListCreateAPIView.as_view()),
    path('<int:pk>/comments/<int:comment_pk>/',
         views.CommentDetailAPIView.as_view()),  # PUT(댓글 수정) & DELETE(댓글 삭제)
    path("<int:pk>/bookmark/", views.BookmarkAPIView.as_view()),
    path("<int:pk>/like/", views.LikesAPIView.as_view()),
]
