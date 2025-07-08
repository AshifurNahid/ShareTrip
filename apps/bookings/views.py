from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings
    Provides CRUD operations and custom actions
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return bookings for current user"""
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Custom creation logic"""
        booking = serializer.save(user=self.request.user)
        return booking
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        if booking.status == 'cancelled':
            return Response(
                {'error': 'Booking already cancelled'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        return Response({
            'message': 'Booking cancelled successfully',
            'booking_id': booking.id
        })

class TripBookingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for trip creators to view bookings for their trips
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return bookings for trips created by current user"""
        trip_id = self.kwargs.get('trip_pk')
        return Booking.objects.filter(
            trip_id=trip_id,
            trip__creator=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, trip_pk=None, pk=None):
        """Confirm a booking (for trip creators)"""
        booking = self.get_object()
        
        if booking.status != 'pending':
            return Response(
                {'error': 'Only pending bookings can be confirmed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'confirmed'
        booking.save()
        
        return Response({
            'message': 'Booking confirmed successfully',
            'booking_id': booking.id
        })