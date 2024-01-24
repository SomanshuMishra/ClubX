# serializers.py
from rest_framework import serializers
from .models import ClubEvent, ClubDetail

class ClubDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubDetail
        fields = ['clubId', 'clubName', 'clubLogo']

class EventSerializer(serializers.ModelSerializer):
    club = ClubDetailSerializer()

    class Meta:
        model = ClubEvent
        fields = ['eventId', 'eventName', 'eventStartDate', 'eventStopDate',
                  'eventDescription', 'eventCoverImage', 'eventVideo', 'club']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['club'] = ClubDetailSerializer(instance.club).data
        return data
