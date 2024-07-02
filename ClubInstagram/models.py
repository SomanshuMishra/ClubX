from django.db import models

# Create your models here.
# models.py

class ClubInstagramMedia(models.Model):
    club_id = models.CharField(max_length=100, db_index=True)
    media_id = models.CharField(max_length=50, unique=True)
    caption = models.TextField(null=True, blank=True)
    media_type = models.CharField(max_length=20)
    media_url = models.URLField(max_length=500)  # Increase the max_length
    thumbnail_url = models.URLField(null=True, blank=True)
    permalink = models.URLField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.media_id
