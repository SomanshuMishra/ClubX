from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClubDetail , Category , ClubEvent, City
from .serializers import ClubDetailSerializer , CategorySerializer , ClubEventSerializer    
from .CitySerializer import CitySerializer

from django.http import Http404

# Create your views here.
def index(request):
    return HttpResponse("Welcome To Clubbers")


class ClubDetailView(APIView):
    def get_object(self, club_id):
        try:
            return ClubDetail.objects.get(pk=club_id)
        except ClubDetail.DoesNotExist:
            raise Http404

    def get(self, request, club_id, format=None):
        club = self.get_object(club_id)
        serializer = ClubDetailSerializer(club)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ActiveCategoryView(APIView):
    def get(self, request, format=None):
        active_categories = Category.objects.filter(status='active')
        serialized_data = CategorySerializer(active_categories, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)


class CustomEventListView(APIView):
    def get_queryset(self, category_id):
        try:
            category = Category.objects.get(pk=category_id)
            return ClubEvent.objects.filter(club__clubCategories=category).order_by('eventStartDate')
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_id, format=None):
        events_by_category = self.get_queryset(category_id)
        serializer = ClubEventSerializer(events_by_category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CityListView(APIView):
    def get(self, request, format=None):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class ClubSearchView(APIView):
    def get(self, request, format=None):
        # Get query parameters
        club_name = request.query_params.get('club_name')

        # Filter clubs based on the provided criteria
        clubs = ClubDetail.objects.filter(status='active')

        if club_name:
            # Perform percentage match search
            clubs = clubs.annotate(
                name_length=Length('clubName'),
                match_count=Length('clubName', filter=Value(club_name, output_field=models.CharField())) * 100 / F('name_length')
            ).filter(match_count__gt=50).order_by('-match_count')[:10]

        serialized_data = self.serialize_clubs(clubs)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def serialize_clubs(self, clubs):
        serialized_data = []

        for club in clubs:
            club_data = ClubDetailSerializer(club).data
            serialized_data.append(club_data)

        return serialized_data