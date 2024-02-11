from django.urls import path
from ClubUsers.views import ClubUserCreateView, ClubUserRetrieveView

urlpatterns = [
    path('save/', ClubUserCreateView.as_view(), name='clubuser-create'),
    path('users/<str:clubberId>/', ClubUserRetrieveView.as_view(), name='retrieve_user'),

]
