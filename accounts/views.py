from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from articles.models import Article

class MyArticleListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        return Article.objects.filter(author=username)
        

class MyBookmarkListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        # 사용자랑 프로필 보려는 사람이랑 같지않으면
        user = User.objects.get(username=username)
        if user != request.user:
            return Response("잘못된 접근입니다. 내 프로필이 맞는지 확인하세요.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Article.objects.filter(user.username)




# Create your views here.
