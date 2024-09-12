from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view()), # refresh_token 발행
    path("", views.AccountsView.as_view()), # 회원가입, 회원탈퇴
    path("login/", views.LoginView.as_view()), # 로그인
    path("logout/", views.LogoutView.as_view()), # 로그아웃
    path("<str:username>", views.UpdateProfileView.as_view()), # 프로필 조회, 회원정보 수정, 비밀번호 변경
]
