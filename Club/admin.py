from django.contrib import admin
from .models import Category, ClubDetail , ClubEvent, EventImage, ClubDetailGallery

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Optional: Customize the way Category model is displayed in the admin
    list_display = ['categoryId', 'categoryName']

@admin.register(ClubDetail)
class ClubDetailAdmin(admin.ModelAdmin):
    list_display = ['clubId', 'clubName', 'address', 'pincode', 'state', 'get_category_names']
    search_fields = ['clubId', 'clubName', 'address', 'pincode', 'state']
    list_filter = ['state']
    filter_horizontal = ['clubCategories']

    def get_category_names(self, obj):
        return ", ".join([category.categoryName for category in obj.clubCategories.all()])
    
    get_category_names.short_description = 'Categories'
    
    
@admin.register(ClubDetailGallery)
class ClubDetailGalleryAdmin(admin.ModelAdmin):
    list_display = ['club', 'gallery']

    def gallery_preview(self, obj):
        return obj.gallery if obj.gallery else None
    
    gallery_preview.short_description = 'Gallery Preview'


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ['event', 'image_preview']

    def image_preview(self, obj):
        return obj.image.url if obj.image else None
    
    image_preview.short_description = 'Image Preview'

@admin.register(ClubEvent)
class ClubEventAdmin(admin.ModelAdmin):
    list_display = ['eventId', 'eventName', 'club', 'eventStartDate', 'eventStopDate']
    search_fields = ['eventId', 'eventName', 'club__clubName']
    list_filter = ['eventStartDate', 'eventStopDate']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('club')

    def club(self, obj):
        return obj.club.clubName