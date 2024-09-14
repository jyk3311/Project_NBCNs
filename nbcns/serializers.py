from rest_framework import serializers
from .models import NBCN

# NBCN 모델


class NBCNSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBCN
        fields = ['id', 'title', 'link', 'content', 'created_at', 'updated_at']
        write_only_fields = ['title', 'link', 'content']
        
