from django.db import models

class Attraction(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    # 添加其他相关字段

    def __str__(self):
        return self.name
