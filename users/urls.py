from django.urls import path
from .views import RegisterView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    # API profile (JWT protected)
    path('profile/', ProfileView.as_view(), name='api_profile'),
]