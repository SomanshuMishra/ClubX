# serializers.py
from rest_framework import serializers
from .models import ClubEvent, ClubDetail, EventImage, Category

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['image']

        
        
class ClubDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubDetail
        fields = ['clubId', 'clubName', 'clubLogo']

class EventSerializer(serializers.ModelSerializer):
    club = ClubDetailSerializer()
    event_images = EventImageSerializer(many=True, read_only=True, source='eventimage_set')
    club_categories = serializers.SerializerMethodField()

    class Meta:
        model = ClubEvent
        fields = ['eventId', 'eventName', 'eventStartDate', 'eventStopDate', 'eventStartTime', 'eventStopTime',
                  'eventDescription', 'eventCoverImage', 'eventVideo', 'club', 'event_images', 'club_categories']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def get_club_categories(self, instance):
        return CategorySerializer(instance.club.clubCategories.all(), many=True).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['categoryId', 'categoryName', 'categoryIcon', 'status']

    