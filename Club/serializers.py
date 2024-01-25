from rest_framework import serializers
from .models import ClubDetail, Category, ClubDetailGallery

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['categoryId', 'categoryName','categoryIcon']


class ClubDetailGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubDetailGallery
        fields = ['gallery']


class ClubDetailSerializer(serializers.ModelSerializer):
    clubCategories = CategorySerializer(many=True)
    club_galleries = ClubDetailGallerySerializer(many=True, read_only=True, source='clubdetailgallery_set')

    class Meta:
        model = ClubDetail
        fields = ['clubId', 'clubName', 'clubDescription', 'clubCoverImage', 'clubLogo',
                  'address', 'pincode', 'state', 'lat', 'lon', 'clubCategories',
                  'facebookUrl', 'instagramUrl', 'twitterUrl', 'club_galleries']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['clubCategories'] = CategorySerializer(instance.clubCategories.all(), many=True).data
        return data
