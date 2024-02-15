from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ClubDetail
from .serializers import ClubDetailSerializer

class ClubSearchView(APIView):
    def get(self, request, format=None):
        # Get category_id from query parameters
        print("check here")
        category_id = request.query_params.get('category_id')
        city = request.query_params.get('city')
        print("city -->" , city)
        print("category_id -->" , category_id)

        # Check if category_id is provided
        if category_id is not None:
            # Filter clubs by category
            clubs = ClubDetail.objects.filter(status='active', clubCategories__categoryId=category_id,city=1)
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
