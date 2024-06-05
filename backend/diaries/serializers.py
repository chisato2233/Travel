from rest_framework import serializers
from .models import DiaryEntry,DiaryRating
from .compress import huff_decompress,huff_compress
import json

from rest_framework import serializers
from .models import DiaryEntry

class DiaryEntrySerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.username', read_only=True)
    userRating = serializers.SerializerMethodField()

    class Meta:
        model = DiaryEntry
        fields = ['id', 'title', 'content', 'date', 'location', 'author', 'rating', 'userRating']

    def get_userRating(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user_rating = DiaryRating.objects.filter(user=request.user, diary_entry=obj).first()
            return user_rating.rating if user_rating else 0  # 返回 0 表示没有评分
        return 0  # 默认返回 0

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['content'] = instance.content  # Assuming the content is already decompressed
        return ret
    
    
    def update(self, instance, validated_data):

        instance.content = validated_data.get('content', instance.content)
        instance.title = validated_data.get('title', instance.title)
        instance.date = validated_data.get('date', instance.date)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance

    def create(self, validated_data):

        return DiaryEntry.objects.create(**validated_data)