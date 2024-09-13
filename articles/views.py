
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, ListAPIView
from .models import Article
from .serializers import ArticleSerializer, ArticleDetailSerializer
from .validators import validate_create


class ArticleListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    pagination_class = PageNumberPagination
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all().order_by("-pk")

    def post(self, request):
        is_valid, error_message = validate_create(request.data)
        if not is_valid:
            return Response(f"{error_message}", status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_superuser and (request.data.get("category") == "Company" and not request.user.is_master):
            return Response({"error_message": "Company 글은 Master만 작성할 수 있습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        article = Article.objects.create(
            title=request.data.get("title"),
            content=request.data.get("content"),
            category=request.data.get("category"),
            author=request.user
        )

        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Article, id=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        if article.author == request.user:
            serializer = ArticleDetailSerializer(
                article, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error_message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        article = self.get_object(pk)
        if article.author == request.user:
            article.soft_delete()
            data = f"{pk}번 게시물 삭제"
            return Response(data)
        else:
            return Response({"error_message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class FreeArticleListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(category='Free').order_by('-pk')


class AskArticleListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(category='Ask').order_by('-pk')


class CompanyArticleListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(category='Company').order_by('-pk')


class BookmarkAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        user = request.user
        if not user in article.bookmark_articles.all():
            article.bookmark_articles.add(request.user)
            return Response("북마크", status=status.HTTP_200_OK)
        else:
            article.bookmark_articles.remove(request.user)  # 북마크 취소
            return Response("북마크 취소됨", status=status.HTTP_200_OK)


class LikesAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)  # 좋아요 취소
            return Response("좋아요 취소됨", status=status.HTTP_200_OK)
        else:
            article.like_users.add(request.user)
            return Response("좋아요", status=status.HTTP_200_OK)
