from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
from .validators import validate_signup, validate_profile
from .serializers import UserSerializer

# 회원가입 및 회원탈퇴
class AccountsView(APIView):
    # 회원가입 및 user 생성
    def post(self, request):
        user_obj = request.user

        # validations(username, password, email)
        is_valid, err_msg = validate_signup(user_obj, request.data)
        if not is_valid:
            return Response({"error": err_msg}, status=status.HTTP_400_BAD_REQUEST)

        # user 생성
        user = User.objects.create_user(
            username=request.data.get("username"),
            password=request.data.get("password"),
            email=request.data.get("email"),
        )

        serializer = UserSerializer(user)
        res_data = serializer.data

        # token 발행
        refresh = RefreshToken.for_user(user)
        res_data["tokens"] = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

        return Response(res_data, status=status.HTTP_201_CREATED)

    # 회원탈퇴(user 비활성화 처리)
    def delete(self, request):
        user = request.user

        password = request.data.get("password")
        if not password or not check_password(password, user.password):
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        user.soft_delete()
        return Response({"success": "계정이 성공적으로 탈퇴되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 로그인
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # 로그인 권한 확인
        user = authenticate(username=username, password=password)

        # validation_username
        if not User.objects.filter(username=username).exists():
            return Response(
                {"error": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        # validation_password
        if not user:
            return Response(
                {"error": "패스워드가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user)
        res_data = serializer.data

        # token 발행
        refresh = RefreshToken.for_user(user)
        res_data["tokens"] = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
        return Response(res_data, status=status.HTTP_200_OK)


# 로그아웃
class LogoutView(APIView):
    def post(self, request):
        refresh_token_str = request.data.get("refresh_token")
        try:
            refresh_token = RefreshToken(refresh_token_str)
        except TokenError:
            return Response({"error": "해당 토큰은 사용할 수 없습니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        refresh_token.blacklist()
        return Response({"success": "로그아웃 되었습니다."},
                        status=status.HTTP_200_OK)


# 프로필 조회, 회원정보 수정, 비밀번호 변경
class UpdateProfileView(APIView):
    # 프로필 조회
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # 회원정보 수정(비밀번호 or 이메일 변경)
    def put(self, request, username):
        user_obj = request.user

        # 사용자가 존재하는지 확인
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."},
                            status=status.HTTP_404_NOT_FOUND)

        # 본인 회원정보만 수정할 수 있도록 체크
        if user != request.user:
            return Response({"message": "수정 권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        # 회원정보 유효성 검사
        is_valid, msg = validate_profile(user_obj, request.data)
        if not is_valid:
            return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호가 유효하다면 비밀번호 설정 및 저장
        new_password = request.data.get("new_password")
        if new_password:
            user.set_password(new_password)

        # 변경 사항 저장
        user.save()

        # 성공 메시지 반환
        return Response({"success": msg}, status=status.HTTP_200_OK)
