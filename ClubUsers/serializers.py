from rest_framework import serializers
from .models import ClubUser, FavouriteEvent

class ClubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubUser
        fields = ['clubberId', 'firstname', 'lastname', 'mobile_number', 'email','image']

    def validate_clubberId(self, value):
        """
        Validate clubberId to ensure it is unique.
        """
        if ClubUser.objects.filter(clubberId=value).exists():
            raise serializers.ValidationError("A user with this clubberId already exists.")
        return value

    def validate_mobile_number(self, value):
        """
        Validate mobile_number to ensure it is unique.
        """
        if ClubUser.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("A user with this mobile number already exists.")
        return value

    def validate_email(self, value):
        """
        Validate email to ensure it is unique.
        """
        if ClubUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

class UpdateClubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubUser
        fields = ['clubberId', 'firstname', 'lastname', 'mobile_number', 'email','image']

    def validate_mobile_number(self, value):
        """
        Validate mobile_number to ensure it is unique.
        """
        # If mobile number is provided and belongs to a different user, raise validation error
        if ClubUser.objects.exclude(pk=self.instance.pk).filter(mobile_number=value).exists():
            raise serializers.ValidationError("A user with this mobile number already exists.")
        return value

    def validate_email(self, value):
        """
        Validate email to ensure it is unique.
        """
        # If email is provided and belongs to a different user, raise validation error
        if ClubUser.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class FavouriteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteEvent
        fields = ['clubUser', 'event']