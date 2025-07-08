from rest_framework import serializers
from .models import Trip, TripImage
from apps.users.serializers import UserSerializer

class TripImageSerializer(serializers.ModelSerializer):
    """
    Serializer for trip images
    Why: Handle image uploads and data
    """
    class Meta:
        model = TripImage
        fields = ['id', 'image', 'caption', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for Trip model
    Why: Handle trip data for API responses
    """
    # Nested serializers - show creator info and images
    creator = UserSerializer(read_only=True)
    images = TripImageSerializer(many=True, read_only=True)
    
    # Calculated fields
    available_spots = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()
    
    class Meta:
        model = Trip
        fields = [
            'id', 'title', 'description', 'destination', 'creator',
            'start_date', 'end_date', 'max_participants', 'price_per_person',
            'image', 'status', 'available_spots', 'is_available', 
            'total_revenue', 'images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['creator', 'created_at', 'updated_at']
    
    def get_available_spots(self, obj):
        """Calculate available spots"""
        return obj.available_spots()
    
    def get_is_available(self, obj):
        """Check if trip is available"""
        return obj.is_available()
    
    def get_total_revenue(self, obj):
        """Get total revenue (only for creator)"""
        request = self.context.get('request')
        if request and request.user == obj.creator:
            return obj.total_revenue()
        return None
    
    def validate(self, attrs):
        """
        Custom validation
        Why: Ensure start date is before end date
        """
        if attrs.get('start_date') and attrs.get('end_date'):
            if attrs['start_date'] >= attrs['end_date']:
                raise serializers.ValidationError(
                    "Start date must be before end date"
                )
        return attrs

class TripCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for trip creation
    Why: Different fields and validation for creation
    """
    class Meta:
        model = Trip
        fields = [
            'title', 'description', 'destination', 'start_date', 
            'end_date', 'max_participants', 'price_per_person', 'image'
        ]
    
    def create(self, validated_data):
        """
        Custom create method
        Why: Automatically set the creator to current user
        """
        request = self.context.get('request')
        validated_data['creator'] = request.user
        return super().create(validated_data)