from rest_framework import serializers
from .models import load_data

class RecommendationSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    recommended_items = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        item_id = validated_data['item_id']
        recommended_items = recommend_items(item_id)
        return {'item_id': item_id, 'recommended_items': recommended_items}