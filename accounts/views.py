from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

# Create your views here.


class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get(
            "username"), password=request.data.get("password"))
        if not user:
            return Response({"error": "아이디나 비밀번호가 틀립니다."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        res_data = serializer.data
        refresh = RefreshToken.for_user(user)
        res_data['refresh_token'] = str(refresh)
        res_data['access_token'] = str(refresh.access_token)
        return Response(res_data)
