from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ClubDetail , ClubEvent
from django.utils import timezone
from .serializers import ClubDetailSerializer
from .EventSerializer import ClubEventSearchSerializer
from django.db.models import F, Value
from django.db.models.functions import Length
from django.db import models  # Add this import


class categoryEventSearchView(APIView):
    def get(self, request, format=None):
        # Get category_id from query parameters
        
        category_id = request.query_params.get('category_id')
        city = request.query_params.get('city')
        print("city -->" , city)
        print("category_id -->" , category_id)

        # Check if category_id is provided
        if category_id is not None:
            # Filter clubs by category
            clubs = ClubDetail.objects.filter(status='active', clubCategories__categoryId=category_id,city=city)
        else:
            # If no category_id provided, return all active clubs
            clubs = ClubDetail.objects.filter(status='active')

        serialized_data = self.serialize_clubs(clubs)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def serialize_clubs(self, clubs):
        serialized_data = []

        for club in clubs:
            club_data = ClubDetailSerializer(club).data
            serialized_data.append(club_data)

        return serialized_data


class ClubSearchView(APIView):
    def get(self, request, format=None):
        # Get required query parameter: city
        city_id = request.query_params.get('city_id')
        
        # Check if city_name is provided
        if not city_id:
            return Response({'error': 'City name is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter clubs based on the provided city_name
        try:
            clubs = ClubDetail.objects.filter(city__id=city_id, status='active')
        except ClubDetail.DoesNotExist:
            return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get additional query parameters
        club_name = request.query_params.get('club_name')

        # Perform additional filtering based on club_name if provided
        if club_name:
            clubs = clubs.filter(clubName__icontains=club_name)[:10]  # Performing case-insensitive partial match search

        serialized_data = self.serialize_clubs(clubs)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def serialize_clubs(self, clubs):
        serialized_data = []

        for club in clubs:
            club_data = {
                'clubId': club.clubId,
                'clubName': club.clubName,
                'clubDescription': club.clubDescription,
                'clubCoverImage': club.clubCoverImage,
                'clubLogo': club.clubLogo
            }
            serialized_data.append(club_data)

        return serialized_data
    
    
class ClubEventSearch(APIView):
    def get(self, request):
        # Get parameters from the request
        city = request.query_params.get('city', None)
        event_name = request.query_params.get('event_name', None)
        current_time = timezone.now()

        if city is None:
            return Response({"error": "City parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Initial queryset with basic filters
        club_events = ClubEvent.objects.filter(
            eventStopDate__gt=current_time,  # Filter events whose stop date is greater than current time
            club__city__id=city,  # Filter events belonging to the specified city
            club__status='active'  # Filter events belonging to active clubs
        )

        # If event name is provided, filter by event name
        if event_name:
            club_events = club_events.filter(eventName__icontains=event_name)

        # Serialize the filtered ClubEvent instances
        serialized_club_events = ClubEventSearchSerializer(club_events, many=True)

        return Response(serialized_club_events.data)
    
    
    