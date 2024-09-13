from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'user', 'created_at')
        read_only_fields = ('user', 'created_at')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'author', 'category', 'created_at')
        read_only_fields = ['title', 'author', 'category']
    def get_bookmark(self, object):
        return object.bookmark_articles.username
    


class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # 게시글에 달린 댓글들을 포함

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'author',
                  'category', 'created_at', 'updated_at', 'comments')
