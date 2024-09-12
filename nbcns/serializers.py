from rest_framework import serializers
from .models import NBCN, NBCN_Bookmark

# NBCN 모델
class NBCNSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBCN
        fields = ['id', 'title', 'link', 'content', 'created_at', 'updated_at']

    # 유효성 검사 메서드를 오버라이드하여 커스텀 유효성 검사 로직을 추가
    def validate(self, data):
        # 'link' 필드가 필수임을 확인하고 없을 경우 ValidationError를 발생시킴
        if not data.get('link'):
            raise serializers.ValidationError({"link": "이 필드는 필수 항목입니다."})
        return data

# NBCN_Bookmark 모델
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBCN_Bookmark
        fields = ['id', 'user', 'NBCN']