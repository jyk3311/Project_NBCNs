from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view()), # refresh_token 발행
    path("", views.AccountsView.as_view()), # 회원가입, 회원탈퇴
    path("login/", views.LoginView.as_view()), # 로그인
    path("logout/", views.LogoutView.as_view()), # 로그아웃
    path("<str:username>", views.UpdateProfileView.as_view()), # 프로필 조회, 회원정보 수정(비밀번호 변경)
    path("<str:username>/my-article/", views.MyArticleListAPIView.as_view()), # 내 작성글 조회
    path("<str:username>/bookmark/", views.MyBookmarkListAPIView.as_view()), # 북마크 조회
]
