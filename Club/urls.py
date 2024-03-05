from django.urls import path , include
from Club import views
from Club.views import ClubDetailView , ActiveCategoryView , CityListView
from Club.EventViews import EventView , EventDetailView , CustomEventListView
from Club.SearchViews import categoryEventSearchView, ClubSearchView, ClubEventSearch


urlpatterns = [
    path('',views.index,name="index"),
    
    # Club APIs
    path('club/<str:club_id>/', ClubDetailView.as_view(), name='club-detail'),
    
    
    # Event APIs
    path('events/', EventView.as_view(), name='event-list'),
    path('event/<str:event_id>/', EventDetailView.as_view(), name='event_detail'),
    path('events/category/<int:category_id>/', CustomEventListView.as_view(), name='custom_event_list'),
    
    
    
    # Search APIs
    path('event-id/', categoryEventSearchView.as_view(), name='club_search'),


    # All Category
    path('active-categories/', ActiveCategoryView.as_view(), name='active_categories'),

    # City API
    path('allCity/', CityListView.as_view(), name='CityListView'),

    # Club Search
    path('clubSearch/', ClubSearchView.as_view(), name='ClubSearchView'),
    
    # Event Search
    path('eventSearch/', ClubEventSearch.as_view(), name='ClubSearchView'),

]

