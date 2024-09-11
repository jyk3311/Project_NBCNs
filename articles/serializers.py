from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'author', 'category', 'created_at')


class ArticleDetailSerializer(ArticleSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'author',
                  'category', 'created_at', 'updated_at')
