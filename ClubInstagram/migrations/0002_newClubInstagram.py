# Generated by Django 5.0.6 on 2024-07-02 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClubInstagram', '0001_update_instagram_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubinstagrammedia',
            name='media_url',
            field=models.URLField(max_length=500),
        ),
    ]
