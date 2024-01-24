from django.db import models

class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=255)
    
    def __str__(self):
        return self.categoryName
    
class ClubDetail(models.Model):
    clubId = models.CharField(max_length=255, primary_key=True)
    clubName = models.CharField(max_length=255)
    clubDescription = models.TextField()
    clubCoverImage = models.CharField(max_length=255, null=True, blank=True)  # Changed to CharField
    clubLogo = models.CharField(max_length=255, null=True, blank=True)  # Changed to CharField
    address = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    clubCategories = models.ManyToManyField(Category, blank=True)
    facebookUrl = models.CharField(max_length=255, null=True, blank=True)
    instagramUrl = models.CharField(max_length=255, null=True, blank=True)
    twitterUrl = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.clubName

class EventImage(models.Model):
    event = models.ForeignKey('ClubEvent', on_delete=models.CASCADE)
    image = models.CharField(max_length=255, null=True, blank=True)  # Changed to CharField

class ClubEvent(models.Model):
    club = models.ForeignKey(ClubDetail, on_delete=models.CASCADE)
    eventId = models.CharField(max_length=255, primary_key=True)
    eventName = models.CharField(max_length=255)
    eventStartDate = models.DateField()
    eventStopDate = models.DateField()
    eventDescription = models.TextField()
    eventCoverImage = models.CharField(max_length=255, null=True, blank=True)  # Changed to CharField
    eventVideo = models.CharField(max_length=255, null=True, blank=True)  # Changed to CharField

    def __str__(self):
        return f"{self.eventName} - {self.club.clubName}"
