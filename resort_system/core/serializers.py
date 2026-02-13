"""
API serializers for future REST API implementation.
This structure can be extended to create REST endpoints.
"""

from rest_framework import serializers
from .models import (
    Amenity, RoomType, Room, Resort, Guest, Reservation, PaymentTransaction
)


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'description', 'icon']


class RoomTypeSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'description', 'base_price', 'capacity', 'amenities']


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'room_type', 'room_number', 'floor', 'status', 'created_at', 'updated_at']


class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = [
            'id', 'name', 'description', 'location', 'city', 'country',
            'phone', 'email', 'website', 'total_rooms', 'check_in_time',
            'check_out_time', 'max_occupancy', 'is_active', 'created_at', 'updated_at'
        ]


class GuestSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = Guest
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'country', 'address', 'guest_type', 'date_joined', 'is_active'
        ]


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'reservation', 'payment_method', 'amount', 'status',
            'transaction_id', 'notes', 'created_at', 'updated_at'
        ]


class ReservationSerializer(serializers.ModelSerializer):
    guest = GuestSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    resort = ResortSerializer(read_only=True)
    payments = PaymentTransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'resort', 'guest', 'room', 'check_in_date', 'check_out_date',
            'number_of_guests', 'status', 'total_nights', 'price_per_night',
            'total_price', 'discount', 'final_price', 'special_requests',
            'notes', 'payments', 'created_at', 'updated_at', 'confirmed_at'
        ]


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new reservations."""
    
    class Meta:
        model = Reservation
        fields = [
            'resort', 'guest', 'room', 'check_in_date', 'check_out_date',
            'number_of_guests', 'special_requests'
        ]
    
    def validate(self, data):
        """Validate reservation data."""
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        room = data.get('room')
        number_of_guests = data.get('number_of_guests')
        
        # Validate dates
        if check_in >= check_out:
            raise serializers.ValidationError("Check-out date must be after check-in date")
        
        # Validate capacity
        if number_of_guests > room.room_type.capacity:
            raise serializers.ValidationError(
                f"Number of guests exceeds room capacity ({room.room_type.capacity})"
            )
        
        # Check availability
        from .utils.validators import check_room_availability
        if not check_room_availability(room, check_in, check_out):
            raise serializers.ValidationError("Room is not available for selected dates")
        
        return data


# Future: ViewSets for REST Framework

"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ResortViewSet(viewsets.ModelViewSet):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    permission_classes = [IsAuthenticated]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def check_availability(self, request):
        '''Check room availability for specific dates'''
        # Implementation here
        pass

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = ReservationCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Create reservation logic
            pass
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        '''Confirm a pending reservation'''
        # Implementation here
        pass
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        '''Cancel a reservation'''
        # Implementation here
        pass

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]

class PaymentTransactionViewSet(viewsets.ModelViewSet):
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [IsAuthenticated]
"""

# To implement REST API:
# 1. Uncomment the ViewSets above
# 2. Create urls.py in the core app with router configuration
# 3. Add REST framework URLs to main urls.py
# 4. Update permissions as needed (e.g., IsAdminUser)
