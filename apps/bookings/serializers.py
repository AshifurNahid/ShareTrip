from rest_framework import serializers
from .models import Booking
from apps.trips.serializers import TripSerializer
from apps.users.serializers import UserSerializer

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model
    Why: Handle booking data with nested trip and user info
    """
    # Nested serializers for complete information
    trip = TripSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    # Trip ID for creation
    trip_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'trip', 'trip_id', 'participants', 
            'total_price', 'status', 'special_requests', 
            'booking_date', 'updated_at'
        ]
        read_only_fields = ['user', 'total_price', 'booking_date', 'updated_at']
    
    def validate_trip_id(self, value):
        """
        Validate trip exists and is available
        Why: Prevent booking unavailable trips
        """
        try:
            trip = Trip.objects.get(id=value, status='published')
        except Trip.DoesNotExist:
            raise serializers.ValidationError("Trip not found or not available")
        
        if not trip.is_available():
            raise serializers.ValidationError("Trip is fully booked")
        
        return value
    
    def validate_participants(self, value):
        """
        Validate number of participants
        Why: Ensure positive number and within limits
        """
        if value < 1:
            raise serializers.ValidationError("At least 1 participant required")
        
        # Check if enough spots available
        trip_id = self.initial_data.get('trip_id')
        if trip_id:
            try:
                trip = Trip.objects.get(id=trip_id)
                if value > trip.available_spots():
                    raise serializers.ValidationError(
                        f"Only {trip.available_spots()} spots available"
                    )
            except Trip.DoesNotExist:
                pass  # Will be caught by trip_id validation
        
        return value
    
    def create(self, validated_data):
        """
        Custom create method
        Why: Set user and calculate total price
        """
        request = self.context.get('request')
        trip_id = validated_data.pop('trip_id')
        
        # Get trip and set user
        trip = Trip.objects.get(id=trip_id)
        validated_data['user'] = request.user
        validated_data['trip'] = trip
        
        # Calculate total price
        validated_data['total_price'] = (
            validated_data['participants'] * trip.price_per_person
        )
        
        return super().create(validated_data)