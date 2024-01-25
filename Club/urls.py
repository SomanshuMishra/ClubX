from django.urls import path , include
from Club import views
from Club.views import ClubDetailView , ActiveCategoryView 
from Club.EventViews import EventView , EventDetailView


urlpatterns = [
    path('',views.index,name="index"),
    path('club/<str:club_id>/', ClubDetailView.as_view(), name='club-detail'),
    path('events/', EventView.as_view(), name='event-list'),
    path('active-categories/', ActiveCategoryView.as_view(), name='active_categories'),
    path('event/<str:event_id>/', EventDetailView.as_view(), name='event_detail'),




]

