from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Trip, TripImage
from .serializers import TripSerializer, TripCreateSerializer, TripImageSerializer

class TripListView(generics.ListAPIView):
    """
    List all published trips
    Why: Show available trips to all users
    What: GET endpoint with filtering and search
    """
    serializer_class = TripSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view trips
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filter fields
    filterset_fields = ['destination', 'status']
    search_fields = ['title', 'description', 'destination']
    ordering_fields = ['start_date', 'price_per_person', 'created_at']
    ordering = ['-created_at']  # Default ordering
    
    def get_queryset(self):
        """
        Filter trips based on parameters
        Why: Only show published trips to regular users
        """
        return Trip.objects.filter(status='published')

class TripDetailView(generics.RetrieveAPIView):
    """
    Get trip details
    Why: Show complete trip information
    What: GET endpoint for single trip
    """
    serializer_class = TripSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Trip.objects.filter(status='published')

class TripCreateView(generics.CreateAPIView):
    """
    Create new trip
    Why: Allow authenticated users to create trips
    What: POST endpoint for trip creation
    """
    serializer_class = TripCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserTripsView(generics.ListAPIView):
    """
    List user's own trips
    Why: Show trips created by the current user
    What: GET endpoint for user's trips (all statuses)
    """
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return trips created by current user"""
        return Trip.objects.filter(creator=self.request.user)

class TripUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update/Delete trip
    Why: Allow trip creators to manage their trips
    What: GET/PUT/PATCH/DELETE endpoints
    """
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Only allow users to update their own trips"""
        return Trip.objects.filter(creator=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_trip_image(request, trip_id):
    """
    Upload additional images for a trip
    Why: Allow trip creators to add multiple images
    What: POST endpoint for image upload
    """
    try:
        trip = Trip.objects.get(id=trip_id, creator=request.user)
    except Trip.DoesNotExist:
        return Response(
            {'error': 'Trip not found or not owned by you'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = TripImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(trip=trip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)