from django.db import models
import random;
class Attraction(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.TextField(db_column='城市')
    name = models.TextField(db_column='名称')  # 假设数据库中的列名是 '名称'
    star_level = models.TextField(db_column='星级')
    rating = models.FloatField(db_column='评分')
    price = models.FloatField(db_column='价格')
    sales = models.IntegerField(db_column='销量')
    province_city_district = models.TextField(db_column='省/市/区')
    coordinates = models.TextField(db_column='坐标')
    description = models.TextField(db_column='简介')
    is_free = models.TextField(db_column='是否免费')
    detailed_address = models.TextField(db_column='具体地址')

    class Meta:
        db_table = 'sheet'
        managed = False  # 告诉 Django 不要管理该表


from django.db import models

class HuffmanCode(models.Model):
    char = models.CharField(max_length=1, unique=True)
    code = models.TextField()

    def __str__(self):
        return f'{self.char}: {self.code}'
