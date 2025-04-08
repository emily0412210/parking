from rest_framework.routers import SimpleRouter,DefaultRouter
from django.urls import path,include
user = DefaultRouter()
from .views import RegisterView,ProfileViewSet,CardViewSet

user.register(r'auth', RegisterView, basename='auth')
user.register(r'profile', ProfileViewSet, basename='profile')
user.register(r'car', CardViewSet, basename='card')

urlpatterns = [
    path('', include(user.urls)),
    
]

