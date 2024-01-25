# serializers.py
from rest_framework import serializers
from .models import ClubEvent, ClubDetail, EventImage

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

    class Meta:
        model = ClubEvent
        fields = ['eventId', 'eventName', 'eventStartDate', 'eventStopDate',
                  'eventDescription', 'eventCoverImage', 'eventVideo', 'club', 'event_images']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


    