# Generated by Django 5.0.3 on 2024-06-02 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HuffmanCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char', models.CharField(max_length=1, unique=True)),
                ('code', models.TextField()),
            ],
        ),
    ]
