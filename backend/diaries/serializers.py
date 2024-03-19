from rest_framework import serializers
from .models import DiaryEntry
from compress import huff_decompress,huff_compress
from rest_framework import serializers
import json

class CompressedTextField(serializers.Field):
    def to_representation(self, value):
        # 从模型实例中提取哈夫曼字典
        huffman_dict = json.loads(self.parent.instance.huffman_dict)
        # 使用哈夫曼字典解压内容
        decompressed_data = huff_decompress(value, huffman_dict)
        return decompressed_data

    def to_internal_value(self, data):
        # 对输入的数据进行压缩
        compressed_data, codes = huff_compress(data)
        # 在模型实例上设置哈夫曼字典
        self.parent.instance.set_huffman_dict(codes)
        return compressed_data



class DiaryEntrySerializer(serializers.ModelSerializer):
    content = CompressedTextField()
    huffman_dict = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = DiaryEntry
        fields = ['id', 'title', 'content', 'date', 'location', 'author']

    def get_author(self, obj):
        # 返回关联用户的用户名
        return obj.user.username
    
    def create(self, validated_data):
        # 使用validated_data创建DiaryEntry实例，这里不需要显式处理huffman_dict
        return DiaryEntry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # 更新DiaryEntry实例，这里不需要显式处理huffman_dict
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
