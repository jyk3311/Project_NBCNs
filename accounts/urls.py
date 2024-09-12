from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>/my-article/", views.MyArticleListAPIView.as_view()),
    path("<str:username>/bookmark/", views.MyBookmarkListAPIView.as_view()),
]
