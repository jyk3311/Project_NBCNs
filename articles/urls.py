from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListCreateAPIView.as_view()),
    path("free/", views.FreeArticleListAPIView.as_view()),
    path("ask/", views.AskArticleListAPIView.as_view()),
    path("<int:pk>", views.ArticleDetailAPIView.as_view()),
]
