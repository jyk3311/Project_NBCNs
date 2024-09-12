from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/bookmark/",views.BookmarkAPIView.as_view()),
    path("<int:pk>/like/", views.LikesAPIView.as_view()),
]
