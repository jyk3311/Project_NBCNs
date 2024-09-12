from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Article
from rest_framework import status


class BookmarkAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.bookmarking.filter(pk=request.user.pk).exists():
            article.bookmarking.remove(request.user)  # 북마크 취소
        else:
            article.bookmarking.add(request.user)
        return Response("성공", status=status.HTTP_200_OK)


class LikesAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)  # 좋아요 취소
        else:
            article.like_users.add(request.user)
        return Response("성공", status=status.HTTP_200_OK)


# Create your views here.
