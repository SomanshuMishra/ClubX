from django.urls import path
from ClubUsers.views import ClubUserCreateView

urlpatterns = [
    path('save/', ClubUserCreateView.as_view(), name='clubuser-create'),
]
