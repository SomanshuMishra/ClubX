from django.contrib import admin
from .models import ClubUser

@admin.register(ClubUser)
class ClubUserAdmin(admin.ModelAdmin):
    list_display = ('clubberId', 'firstname', 'lastname', 'mobile_number', 'email')
