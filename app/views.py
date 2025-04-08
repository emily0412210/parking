from rest_framework.viewsets import ViewSet, ModelViewSet
from .serializers import RegisterParkingSerializer, BookingSerializer, ParkingShortSerializer,ParkingDetailSerializer
from .models import Parking
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count,Q
from rest_framework.response import Response
 
class RegisterParkingViewSet(ModelViewSet):
    
    serializer_class = RegisterParkingSerializer
    http_method_names = ['get','post']
    parser_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Parking.objects.filter(owner = self.request.user)
    
    
    def perform_create(self, serializer):
        data = serializer.save(owner = self.request.user)
        return data 
    
class BookingSlot(ViewSet):
    @action(methods=['POST'], detail=False)
    def book(self,request,*args,**kwargs):
        serializer = BookingSerializer(data = request.data , context={"request" : request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save(action='book')
        ss =BookingSerializer (data)
        return Response(ss.data)
    

    @action(methods=['POST'], detail=False)
    def arrive(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save(action='arrive')
        response_serializer = BookingSerializer(data)
        return Response(response_serializer.data)
    
    @action(methods=['POST'], detail=False)
    def left(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save(action='left')
        response_serializer = BookingSerializer(data)
        return Response(response_serializer.data)
        
    @action(methods=['POST'], detail=False)
    def reject(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save(action='reject')
        response_serializer = BookingSerializer(data)
        return Response(response_serializer.data)
