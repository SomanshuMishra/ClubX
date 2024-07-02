from ClubInstagram import views
from django.urls import path 
from ClubInstagram.views import get_instagram_data

urlpatterns = [
    path('callback/', views.handle_instagram_callback, name='instagram_callback'),
    path('initiateIngram/', views.initiate_instagram_auth, name='initiate_instagram_auth'),
    path('get_instagram_data/', views.get_instagram_data, name='get_instagram_data'),
    path('save_instagram_data/', views.save_instagram_data, name='save_instagram_data'),
]