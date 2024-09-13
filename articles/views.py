
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
from django.db.models import Count
from nbcns.models import NBCN
from nbcns.serializers import NBCNSerializer


# 게시물 목록 조회, 게시물 등록
class ArticleListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        res_data = {}
        # 메인 페이지에서 nbcns의 최신 게시물 5개와, 인기 게시물 5개를 보여줌
        nbcns = NBCN.objects.all().order_by("-pk")[:5]
        nbcns_seri5 = NBCNSerializer(nbcns, many=True)
        articles = Article.objects.annotate(likes_count=Count("like_users")).order_by(
            "-likes_count", "-created_at"
        )[:5]
        article_seri5 = ArticleSerializer(articles, many=True)
        res_data['nbcns'] = nbcns_seri5.data
        res_data['articles'] = article_seri5.data
        return Response(res_data, status=status.HTTP_200_OK)

    def post(self, request):
        # 유효성 검증
        is_valid, error_message = validate_create(request.data)
        if not is_valid:
            return Response(f"{error_message}", status=status.HTTP_400_BAD_REQUEST)

        # 관리자인지 확인하고 아니라면 카테고리가 Company인지 user가 마스터인지 확인함
        if not request.user.is_superuser and (request.data.get("category") == "Company" and not request.user.is_master):
            return Response({"message": "Company 글은 Master만 작성할 수 있습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        article = Article.objects.create(
            title=request.data.get("title"),
            content=request.data.get("content"),
            category=request.data.get("category"),
            author=request.user
        )

        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 게시물 상세 조회, 수정, 삭제
class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # url에서 보낸 pk값으로 게시물을 찾음
    def get_object(self, pk):
        return get_object_or_404(Article, id=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    # 수정, 삭제시 게시물 작성자가 로그인한 유저와 일치한지 확인하고 아니라면 허락하지 않음
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
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        article = self.get_object(pk)
        if article.author == request.user:
            # 실제로 데이터베이스에서 삭제하는게 아니라 비활성화 시켜서 조회가 안되도록 함
            article.soft_delete()
            return Response({"success": "성공적으로 삭제되었습니다."})
        else:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


# 카테고리별 게시판 조회
class CategoryArticleListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        # GET 요청으로 sort 매개변수값 가져옴/ 기본값은 '-created_at'
        sort_option = self.request.GET.get('sort', '-created_at')
        if sort_option == '-created_at':
            return Article.objects.filter(category=category).order_by(
                '-created_at')
        else:
            # 테이블에 likes_count라는 컬럼이 없는데 우리가 조회할때 임시로 만들어서 쓰는게 annotate->order_by해서 products에 넣음
            return Article.objects.filter(category=category).annotate(likes_count=Count("like_users")).order_by(
                "-likes_count", "-created_at"
            )


class BookmarkAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        user = request.user
        if not user in article.bookmark_users.all():
            article.bookmark_users.add(request.user)
            return Response({"message": "북마크"}, status=status.HTTP_200_OK)
        else:
            article.bookmark_users.remove(request.user)  # 북마크 취소
            return Response({"message": "북마크 취소됨"}, status=status.HTTP_200_OK)


class LikesAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)  # 좋아요 취소
            return Response({"message": "좋아요 취소됨"}, status=status.HTTP_200_OK)
        else:
            article.like_users.add(request.user)
            return Response({"message": "좋아요"}, status=status.HTTP_200_OK)


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
        # 작성자만 댓글 수정 가능
        if comment.user != request.user:
            return Response({"message": "댓글을 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 댓글 데이터를 요청 데이터로 업데이트 (부분 업데이트 가능)
        serializer = CommentSerializer(
            comment, data=request.data, partial=True)
        # 유효성 검사
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, comment_pk):
        comment = self.get_object(pk, comment_pk)

        # 작성자만 댓글 삭제 가능
        if comment.user != request.user:
            return Response({"message": "댓글을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # Soft delete (실제 삭제 대신 is_mine 필드를 False로 설정)
        comment.soft_delete()

        return Response({"message": "댓글이 소프트 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
