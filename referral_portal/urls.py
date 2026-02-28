from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import home, login_view, logout_view,signup_view

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/referrals/', include('referrals.urls')),
    path('signup/', signup_view, name='signup'),
]