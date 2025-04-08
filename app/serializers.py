from rest_framework import serializers
from .models import Parking,Floor,Slot,Booking


class FloorSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    suffix = serializers.CharField()
    slots = serializers.IntegerField()


    def validate_number(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number must be a positive integer.")
        if value > 20:
            raise serializers.ValidationError("Number should be at most 20.")
        return value

    def validate_suffix(self, value):
        if len(value) > 2:
            raise serializers.ValidationError("Suffix should be at most 2 characters long.")
        return value

    def validate_slots(self, value):
        if value <= 0:
            raise serializers.ValidationError("Slots must be a positive integer.")
        if value > 100:
            raise serializers.ValidationError("Slots should be at most 100.")
        return value

class RegisterParkingSerializer(serializers.ModelSerializer):
    
    
    floors = serializers.ListField(child= FloorSerializer() ,write_only = True)
    
    class Meta:
        model = Parking
        exclude = ['owner','status']
        
    def create(self, validated_data):
        floors = validated_data.pop('floors',[])
        parking=  super().create(validated_data)
        
        for floor in floors:
            slots = floor.pop("slots")
            floor = Floor.objects.create(**floor,parking = parking)
            slots = [Slot(floor = floor, number = i) for i in range(1,slots +1)]
            Slot.objects.bulk_create(slots,batch_size=500)
        return parking
     
class ParkingShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parkingexclude = ["owner"]

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        models = Slot
        fields = "__all__"

class FloorSerializer(serializers.ModelSerializer):
    slot_set = SlotSerializer(many =True)
    class Meta:
        model = Floor
        fields = "__all__"

class ParkingDetailSerializer(serializers.ModelSerializer):
    floor_count = serializers.ReadOnlyField()
    free_slot = serializers.ReadOnlyField()
    floors = FloorSerializer(many = True)

    class Meta:
        model = Parking
        exclude = ['owner']
        
class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = ['car_number','slot']
        extra_kwargs = {
            'car_number' : {"required" : False}
        }
        
        
    def save(self, **kwargs):
        user = self.context['request'].user
        slot = self.validated_data['slot']
        
        action = kwargs.get("action","book")
        if action == 'book':
            
            slot.status = True
            slot.save()

            if user.is_authenticated:
                self.validated_data["car_number"] = user.car_number
            else:
                if not self.validated_data.get("car_number", None):
                    raise serializers.ValidationError("car_number must be set")
            booking ,_= Booking.objects.get_or_create(**self.validated_data, status  = 'booked')
            return  booking
        
class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields  = '__all__'
        depth = 3
