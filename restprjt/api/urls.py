from django.urls import path
from .views import UserRegistration, MyTokenObtainPairView, UserProfile, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/',UserRegistration.as_view(),name='register'),
    path('login/',MyTokenObtainPairView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('profile/',UserProfile.as_view(),name='profile'),
    path('userprofile/',UserProfileView.as_view(),name='userprofile'),
    path('userprofile/<int:pk>/',UserProfileView.as_view(),name='userprofileedit'),
]
