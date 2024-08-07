from django.db import models
from  Club.models import ClubEvent, City


class ClubUser(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

    clubberId = models.CharField(primary_key=True, max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    dob = models.DateField(blank=True,null =True)
    city = models.ForeignKey(City,on_delete=models.DO_NOTHING,blank=True,null =True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES,null=True,blank=True)
    image = models.CharField( max_length=250,null=True,blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class FavouriteEvent(models.Model):
    clubUser = models.ForeignKey(ClubUser, on_delete=models.CASCADE)
    event = models.ForeignKey(ClubEvent, on_delete=models.CASCADE)
        
    def __unicode__(self):
        return self.clubUser.firstname

