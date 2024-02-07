from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ClubUser
from .serializers import ClubUserSerializer

class ClubUserCreateView(APIView):
    def post(self, request, format=None):
        serializer = ClubUserSerializer(data=request.data)
        if serializer.is_valid():
            club_user = serializer.save()
            serialized_data = ClubUserSerializer(club_user).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
