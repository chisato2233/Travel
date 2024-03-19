from django.db import models
from django.contrib.auth.models import User
import json

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diaries')  # 关联到User模型
    title = models.CharField(max_length=255)
    content = models.BinaryField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    huffman_dict = models.TextField()  # 存储哈夫曼字典的JSON字符串

    def set_huffman_dict(self, huffman_dict):
        self.huffman_dict = json.dumps(huffman_dict)

    def get_huffman_dict(self):
        return json.loads(self.huffman_dict)

    def __str__(self):
        return self.title
