from django.db import models
from django.contrib.auth.models import User
import json
from .compress import huff_compress, huff_decompress

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diaries')  # 关联到User模型
    title = models.CharField(max_length=255)
    content = models.TextField()  # 存储原始日记内容
    date = models.DateField()
    location = models.CharField(max_length=255)
    huffman_dict = models.TextField()  # 存储哈夫曼字典的JSON字符串
    huffman_data = models.BinaryField()  # 存储被哈夫曼压缩的数据
    total_rating = models.IntegerField(default=0)  # 总评分

    def set_huffman_dict(self, huffman_dict):
        self.huffman_dict = json.dumps(huffman_dict)

    def get_huffman_dict(self):
        return json.loads(self.huffman_dict)

    def save(self, *args, **kwargs):
        if self.content:
            compressed_data, huffman_dict = huff_compress(self.content)
            self.huffman_data = compressed_data
            self.set_huffman_dict(huffman_dict)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class DiaryRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    diary_entry = models.ForeignKey(DiaryEntry, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()  # -1 for dislike, +1 for like

    class Meta:
        unique_together = ('user', 'diary_entry')
