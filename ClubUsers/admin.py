from django.contrib import admin
from .models import ClubUser, FavouriteEvent

@admin.register(ClubUser)
class ClubUserAdmin(admin.ModelAdmin):
    list_display = ('clubberId', 'firstname', 'lastname', 'mobile_number', 'email')

class FavouriteEventAdmin(admin.ModelAdmin):
    list_display = ['clubUser', 'event']

admin.site.register(FavouriteEvent, FavouriteEventAdmin)