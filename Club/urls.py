from django.urls import path , include
from Club import views
from Club.views import ClubDetailView , ActiveCategoryView 
from Club.EventViews import EventView , EventDetailView , CustomEventListView
from Club.SearchViews import ClubSearchView


urlpatterns = [
    path('',views.index,name="index"),
    
    # Club APIs
    path('club/<str:club_id>/', ClubDetailView.as_view(), name='club-detail'),
    
    
    # Event APIs
    path('events/', EventView.as_view(), name='event-list'),
    path('event/<str:event_id>/', EventDetailView.as_view(), name='event_detail'),
    path('events/category/<int:category_id>/', CustomEventListView.as_view(), name='custom_event_list'),
    
    
    
    # Search APIs
    path('api/club-search/', ClubSearchView.as_view(), name='club_search'),


    # All Category
    path('active-categories/', ActiveCategoryView.as_view(), name='active_categories'),




]

