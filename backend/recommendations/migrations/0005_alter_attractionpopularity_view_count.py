# Generated by Django 5.0.6 on 2024-06-05 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0004_alter_attractionpopularity_view_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attractionpopularity',
            name='view_count',
            field=models.IntegerField(default=61),
        ),
    ]