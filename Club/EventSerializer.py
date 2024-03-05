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


class ClubEventSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubEvent
        fields = ['eventId', 'eventName', 'eventStartDate', 'eventStartTime', 'eventStopDate', 'eventStopTime', 'eventDescription', 'eventCoverImage', 'eventVideo', 'club']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['club'] = {
    #         'clubId': instance.club.clubId,
    #         'clubName': instance.club.clubName,
    #         'clubDescription': instance.club.clubDescription,
    #         'clubCoverImage': instance.club.clubCoverImage,
    #         'clubLogo': instance.club.clubLogo,
    #         'address': instance.club.address,
    #         'pincode': instance.club.pincode,
    #         # 'state': instance.club.state.stateName if instance.club.state else None,
    #         # 'city': instance.club.city.cityName if instance.club.city else None,
    #         'lat': str(instance.club.lat),
    #         'lon': str(instance.club.lon),
    #         'clubCategories': [category.categoryName for category in instance.club.clubCategories.all()],
    #         'facebookUrl': instance.club.facebookUrl,
    #         'instagramUrl': instance.club.instagramUrl,
    #         'twitterUrl': instance.club.twitterUrl,
    #         'status': instance.club.status
    #     }
    #     return representation
    
    