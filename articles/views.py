from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from .models import Article
from .serializers import ArticleSerializer
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
        article = Article.objects.create(
            title=request.data.get("title"),
            content=request.data.get("content"),
            category=request.data.get("category"),
            author=request.user
        )

        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
