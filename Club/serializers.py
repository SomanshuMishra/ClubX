from rest_framework import serializers
from .models import ClubDetail, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['categoryId', 'categoryName']

class ClubDetailSerializer(serializers.ModelSerializer):
    clubCategories = CategorySerializer(many=True)

    class Meta:
        model = ClubDetail
        fields = ['clubId', 'clubName', 'clubDescription', 'clubCoverImage', 'clubLogo',
                  'address', 'pincode', 'state', 'lat', 'lon', 'clubCategories',
                  'facebookUrl', 'instagramUrl', 'twitterUrl']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['clubCategories'] = CategorySerializer(instance.clubCategories.all(), many=True).data
        return data
