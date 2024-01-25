from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClubDetail , Category
from .serializers import ClubDetailSerializer , CategorySerializer
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
