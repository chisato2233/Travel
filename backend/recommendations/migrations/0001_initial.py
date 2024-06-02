# Generated by Django 5.0.3 on 2024-06-02 16:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backend', '0002_huffmancode'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttractionPopularity',
            fields=[
                ('attraction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='popularity', serialize=False, to='backend.attraction')),
                ('view_count', models.IntegerField(default=65)),
            ],
        ),
        migrations.CreateModel(
            name='UserSearchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_time', models.DateTimeField(auto_now_add=True)),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.attraction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
