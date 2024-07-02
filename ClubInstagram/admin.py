from django.contrib import admin
from .models import ClubInstagramMedia

@admin.register(ClubInstagramMedia)
class ClubInstagramMediaAdmin(admin.ModelAdmin):
    list_display = ('media_id', 'club_id', 'caption', 'media_type', 'media_url', 'timestamp')
    search_fields = ('media_id', 'club_id', 'caption')
    list_filter = ('media_type', 'timestamp')
    ordering = ('-timestamp',)
