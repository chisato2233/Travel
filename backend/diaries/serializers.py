from rest_framework import serializers
from .models import DiaryEntry
from .compress import huff_decompress, huff_compress
import json

class CompressedTextField(serializers.Field):
    def to_representation(self, value):
        instance = self.parent.instance
        huffman_dict = json.loads(instance.huffman_dict)
        decompressed_data = huff_decompress(value, huffman_dict)
        return decompressed_data

    def to_internal_value(self, data):
        compressed_data, huffman_dict = huff_compress(data)
        self.context['huffman_dict'] = huffman_dict
        return memoryview(compressed_data)

class DiaryEntrySerializer(serializers.ModelSerializer):
    content = CompressedTextField()
    author = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = DiaryEntry
        fields = ['id', 'title', 'content', 'date', 'location', 'author']

    def create(self, validated_data):
        huffman_dict = self.context.get('huffman_dict', {})
        validated_data['huffman_dict'] = json.dumps(huffman_dict)
        return DiaryEntry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'content' in validated_data:
            compressed_content, huffman_dict = validated_data.pop('content')
            instance.content = memoryview(compressed_content)
            instance.huffman_dict = json.dumps(huffman_dict)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
