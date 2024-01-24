from django.urls import path , include
from Club import views
from Club.views import ClubDetailView 
from Club.EventViews import EventView


urlpatterns = [
    path('',views.index,name="index"),
    path('club/<str:club_id>/', ClubDetailView.as_view(), name='club-detail'),
    path('events/', EventView.as_view(), name='event-list'),


]

