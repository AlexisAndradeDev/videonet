# Generated by Django 5.0 on 2024-11-04 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
    ]