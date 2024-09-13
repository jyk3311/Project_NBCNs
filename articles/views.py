from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, ListAPIView
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentSerializer
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
    

# 특정 게시글에 대한 댓글 목록 조회 및 댓글 작성
class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 특정 게시글에 달린 모든 댓글을 조회
    def get(self, request, pk):
        # 특정 게시글과 댓글 가져오기
        article = Article.objects.get(pk=pk)
        comments = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # 특정 게시글에 댓글 작성
    def post(self, request, pk):
        # 특정 게시글을 가져오고 request.data 직렬화
        article = Article.objects.get(pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():  # 유효성 검사
            serializer.save(user=request.user, article=article)  # 작성자와 게시글을 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 특정 댓글 수정 및 삭제
class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 해당 댓글 객체 가져오기
    def get_object(self, pk, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk, article__pk=pk)

    def put(self, request, pk, comment_pk):
        comment = self.get_object(pk, comment_pk)
        # 작성자만 댓글을 수정할 수 있음
        if comment.user != request.user:
            return Response({"error_message": "댓글을 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 댓글 데이터를 요청 데이터로 업데이트 (부분 업데이트 가능)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        # 유효성 검사
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

