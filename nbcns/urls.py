from django.urls import path
from .views import NBCNListCreateAPIView, NBCNDetailAPIView, NBCNBookmarkAPIView

urlpatterns = [
    path('', NBCNListCreateAPIView.as_view()),
    path('<int:pk>/', NBCNDetailAPIView.as_view()),
    path('<int:pk>/bookmark/', NBCNBookmarkAPIView.as_view()),
]