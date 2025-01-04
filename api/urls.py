from django.urls import path
from .views import get_api_data

urlpatterns = [
    path('data/', get_api_data, name='get_api_data'),
]