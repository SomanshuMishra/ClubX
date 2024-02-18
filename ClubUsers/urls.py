from django.urls import path
from ClubUsers.views import ClubUserCreateView, ClubUserRetrieveView , FavouriteEventAPI, ClubUserUpdateView

urlpatterns = [
    path('save/', ClubUserCreateView.as_view(), name='clubuser-create'),
    path('updateUser/<str:pk>/', ClubUserUpdateView.as_view(), name='club-user-update'),

    path('users/<str:clubberId>/', ClubUserRetrieveView.as_view(), name='retrieve_user'),
    path('favourite-events/', FavouriteEventAPI.as_view(), name='favourite-events-api'),


]
