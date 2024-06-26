# Generated by Django 5.0.3 on 2024-06-02 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('city', models.TextField(db_column='城市')),
                ('name', models.TextField(db_column='名称')),
                ('star_level', models.TextField(db_column='星级')),
                ('rating', models.FloatField(db_column='评分')),
                ('price', models.FloatField(db_column='价格')),
                ('sales', models.IntegerField(db_column='销量')),
                ('province_city_district', models.TextField(db_column='省/市/区')),
                ('coordinates', models.TextField(db_column='坐标')),
                ('description', models.TextField(db_column='简介')),
                ('is_free', models.TextField(db_column='是否免费')),
                ('detailed_address', models.TextField(db_column='具体地址')),
            ],
            options={
                'db_table': 'sheet',
                'managed': False,
            },
        ),
    ]
