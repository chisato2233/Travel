from rest_framework import serializers
from .models import GeneratedVideo

class GeneratedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedVideo
        fields = ['id', 'user', 'generation_id', 'status', 'video_data', 'seed', 'created_at']
