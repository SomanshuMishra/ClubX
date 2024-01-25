# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClubEvent
from Club.EventSerializer import EventSerializer

class EventView(APIView):
    def get(self, request, format=None):
        events = ClubEvent.objects.filter(club__status='active')
        serialized_data = self.serialize_events(events)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def serialize_events(self, events):
        serialized_data = []
        club_map = {}

        for event in events:
            club_id = event.club.clubId
            if club_id not in club_map:
                club_map[club_id] = {
                    'clubId': club_id,
                    'clubName': event.club.clubName,
                    'clubLogo': event.club.clubLogo if event.club.clubLogo else None,
                    'events': []
                }

            event_data = EventSerializer(event).data
            club_map[club_id]['events'].append(event_data)

        for club_id, club_data in club_map.items():
            serialized_data.append({
                'clubId': club_id,
                'clubName': club_data['clubName'],
                'clubLogo': club_data['clubLogo'],
                'events': club_data['events']
            })

        return serialized_data
