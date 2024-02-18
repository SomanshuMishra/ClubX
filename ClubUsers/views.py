from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ClubUser
from .serializers import ClubUserSerializer, FavouriteEventSerializer, UpdateClubUserSerializer


# Create User
class ClubUserCreateView(APIView):
    def post(self, request, format=None):
        serializer = ClubUserSerializer(data=request.data)
        if serializer.is_valid():
            club_user = serializer.save()
            serialized_data = ClubUserSerializer(club_user).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update User
class ClubUserUpdateView(APIView):
    def put(self, request, pk, format=None):
        try:
            club_user = ClubUser.objects.get(pk=pk)
        except ClubUser.DoesNotExist:
            return Response({"error": "ClubUser not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateClubUserSerializer(club_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  Get User Details
class ClubUserRetrieveView(APIView):
    def get(self, request, clubberId, format=None):
        try:
            user = ClubUser.objects.get(clubberId=clubberId)
            serializer = ClubUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClubUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Save Favourite Event
class FavouriteEventAPI(APIView):
    def post(self, request, format=None):
        serializer = FavouriteEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)