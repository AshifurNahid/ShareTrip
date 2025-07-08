from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for user profile
    Why: Allows users to view and update their profile
    What: GET/PUT/PATCH endpoints for user profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Return the current user"""
        return self.request.user

class UserCreateView(generics.CreateAPIView):
    """
    View for user registration
    Why: Allow new users to register
    What: POST endpoint for user creation
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can register

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    Get user statistics
    Why: Provide dashboard data for users
    What: Returns trips created, bookings made, etc.
    """
    user = request.user
    
    # Count user's trips and bookings
    trips_created = user.created_trips.count()
    bookings_made = user.bookings.count()
    
    # Get recent activity
    recent_trips = user.created_trips.order_by('-created_at')[:5]
    recent_bookings = user.bookings.order_by('-booking_date')[:5]
    
    return Response({
        'trips_created': trips_created,
        'bookings_made': bookings_made,
        'recent_trips': [
            {'id': trip.id, 'title': trip.title, 'destination': trip.destination}
            for trip in recent_trips
        ],
        'recent_bookings': [
            {'id': booking.id, 'trip_title': booking.trip.title, 'status': booking.status}
            for booking in recent_bookings
        ]
    })