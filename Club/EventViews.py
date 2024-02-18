# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClubEvent, Category
from Club.EventSerializer import EventSerializer
from Club.EventDetailSerializer import EventDetailSerializer
from .serializers import ClubEventSerializer
from django.http import Http404
from datetime import date
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from django.core.serializers import serialize
from django.http import JsonResponse
import json

 
# Pagination API

# class EventView(APIView, PageNumberPagination):
#     page_size = 10  # Set the number of events per page

#     def get(self, request, format=None):
#         events = ClubEvent.objects.filter(club__status='active')
#         paginated_events = self.paginate_queryset(events, request)
#         serialized_data = self.serialize_events(paginated_events)
#         return self.get_paginated_response(serialized_data)

#     def serialize_events(self, events):
#         serialized_data = []
#         club_map = {}

#         for event in events:
#             club_id = event.club.clubId
#             if club_id not in club_map:
#                 club_map[club_id] = {
#                     'clubId': club_id,
#                     'clubName': event.club.clubName,
#                     'clubLogo': event.club.clubLogo if event.club.clubLogo else None,
#                     'events': []
#                 }

#             event_data = EventSerializer(event).data
#             club_map[club_id]['events'].append(event_data)

#         for club_id, club_data in club_map.items():
#             serialized_data.append({
#                 'clubId': club_id,
#                 'clubName': club_data['clubName'],
#                 'clubLogo': club_data['clubLogo'],
#                 'events': club_data['events']
#             })

#         return serialized_data


# class EventView(APIView):
#     def get(self, request, format=None):
#         events = ClubEvent.objects.filter(club__status='active')
#         serialized_data = self.serialize_events(events)
#         return Response(serialized_data, status=status.HTTP_200_OK)

#     def serialize_events(self, events):
#         serialized_data = []
#         club_map = {}

#         for event in events:
#             club_id = event.club.clubId
#             if club_id not in club_map:
#                 club_map[club_id] = {
#                     'clubId': club_id,
#                     'clubName': event.club.clubName,
#                     'clubLogo': event.club.clubLogo if event.club.clubLogo else None,
#                     'events': []
#                 }

#             event_data = EventSerializer(event).data
#             club_map[club_id]['events'].append(event_data)

#         for club_id, club_data in club_map.items():
#             serialized_data.append({
#                 'clubId': club_id,
#                 'clubName': club_data['clubName'],
#                 'clubLogo': club_data['clubLogo'],
#                 'events': club_data['events']
#             })

#         return serialized_data


class EventView(APIView):
    def get(self, request, format=None):
        current_time = timezone.now()
        city = request.query_params.get('city')  # Assuming city is passed as a query parameter
        events = ClubEvent.objects.filter(club__status='active', club__city__id=1,eventStopDate__gt=current_time).order_by('eventStartDate')
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

# class EventDetailView(APIView):
#     def get(self, request, event_id, format=None):
#         try:
#             event = ClubEvent.objects.get(eventId=event_id)
#         except ClubEvent.DoesNotExist:
#             return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

#         serialized_data = EventSerializer(event).data
#         return Response(serialized_data, status=status.HTTP_200_OK)
    
  
class EventDetailView(APIView):
    def get(self, request, event_id, format=None):
        try:
            event = ClubEvent.objects.get(eventId=event_id)
        except ClubEvent.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        serialized_data = EventDetailSerializer(event, context={'request': request}).data

        # Fetch similar events queryset
        similar_events_queryset = EventDetailSerializer().get_similar_events(event)

        # Exclude current event from similar events queryset
        similar_events_queryset = similar_events_queryset.exclude(eventId=event_id)

        # Convert queryset to set to remove duplicates
        similar_events_queryset = set(similar_events_queryset)

        # Serialize similar events
        serialized_similar_events = serialize('json', similar_events_queryset)

        # Convert JSON string to list of dictionaries
        similar_events_list = json.loads(serialized_similar_events)

        # Sort similar events based on eventStartDate
        sorted_similar_events = sorted(similar_events_list, key=lambda x: x['fields']['eventStartDate'])

        # Remove "model" key from each event
        for event in sorted_similar_events:
            del event['model']

        # Directly include sorted similar events in response data
        serialized_data['similar_events'] = sorted_similar_events

        return JsonResponse(serialized_data, status=status.HTTP_200_OK)

  
class CustomEventListView(APIView):
    def get_queryset(self, category_id):
        try:
            category = Category.objects.get(pk=category_id)
            today = timezone.now().date()
            return ClubEvent.objects.filter(
                club__status='active',
                club__clubCategories=category,
                eventStopDate__gte=today  # Exclude events where today's date is greater than eventStopDate
            ).order_by('eventStartDate')
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_id, format=None):
        events_by_category = self.get_queryset(category_id)
        serializer = ClubEventSerializer(events_by_category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
