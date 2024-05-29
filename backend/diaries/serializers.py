from rest_framework import serializers
from .models import DiaryEntry
from .compress import huff_decompress,huff_compress
import json

from rest_framework import serializers
from .models import DiaryEntry

class DiaryEntrySerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = DiaryEntry
        fields = ['id', 'title', 'content', 'date', 'location', 'author']

    def to_representation(self, instance):
       
        ret = super().to_representation(instance)
        ret['content'] = instance.content  
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