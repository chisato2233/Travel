# Generated by Django 5.0.6 on 2024-06-05 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_generatedvideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedvideo',
            name='seed',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
