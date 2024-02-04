from rest_framework import serializers
from .models import ClubDetail, Category, ClubDetailGallery , ClubEvent

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['categoryId', 'categoryName','categoryIcon']


class ClubDetailGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubDetailGallery
        fields = ['gallery']


class ClubDetailSerializer(serializers.ModelSerializer):
    clubCategories = CategorySerializer(many=True)
    club_galleries = ClubDetailGallerySerializer(many=True, read_only=True, source='clubdetailgallery_set')
    events = serializers.SerializerMethodField()

    class Meta:
        model = ClubDetail
        fields = ['clubId', 'clubName', 'clubDescription', 'clubCoverImage', 'clubLogo',
                  'address', 'pincode', 'state', 'lat', 'lon', 'clubCategories',
                  'facebookUrl', 'instagramUrl', 'twitterUrl', 'club_galleries', 'events']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['clubCategories'] = CategorySerializer(instance.clubCategories.all(), many=True).data
        return data

    def get_events(self, instance):
        events = ClubEvent.objects.filter(club=instance)
        serializer = ClubEventSerializer(events, many=True)
        return serializer.data
    
class ClubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubEvent
        fields = ['eventId', 'eventName', 'club', 'eventStartDate', 'eventStartTime', 'eventStopDate', 'eventStopTime', 'eventDescription', 'eventCoverImage', 'eventVideo']



