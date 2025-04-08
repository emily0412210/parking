from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import RegisterParkingViewSet,BookingSlot


app = DefaultRouter()

app.register(r'register-parking', RegisterParkingViewSet, basename='register-parking')
app.register(r'booking', BookingSlot, basename='booking')

urlpatterns = [
    path('', include(app.urls)),
    
]



