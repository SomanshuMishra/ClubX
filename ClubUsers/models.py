from django.db import models

class ClubUser(models.Model):
    clubberId = models.CharField(primary_key=True, max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
