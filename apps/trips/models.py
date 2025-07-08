from django.db import models
from django.conf import settings

class Trip(models.Model):
    """
    Trip model represents a travel trip
    OOP Concept: Encapsulation - all trip data in one class
    """
    
    # Trip status choices - demonstrates Django choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    destination = models.CharField(max_length=100)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,  # If user deleted, delete their trips
        related_name='created_trips'  # Access trips from user: user.created_trips.all()
    )
    
    # Trip details
    start_date = models.DateField()
    end_date = models.DateField()
    max_participants = models.PositiveIntegerField()
    price_per_person = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # OOP Concept: Method - behavior of the class
    def __str__(self):
        return f"{self.title} - {self.destination}"
    
    def is_available(self):
        """Check if trip is available for booking"""
        from .bookings.models import Booking
        current_bookings = Booking.objects.filter(
            trip=self, 
            status='confirmed'
        ).count()
        return current_bookings < self.max_participants
    
    def available_spots(self):
        """Calculate available spots"""
        from apps.bookings.models import Booking
        confirmed_bookings = Booking.objects.filter(
            trip=self, 
            status='confirmed'
        ).count()
        return self.max_participants - confirmed_bookings
    
    def total_revenue(self):
        """Calculate total revenue from confirmed bookings"""
        from apps.bookings.models import Booking
        confirmed_bookings = Booking.objects.filter(
            trip=self, 
            status='confirmed'
        ).count()
        return confirmed_bookings * self.price_per_person
    
    class Meta:
        db_table = 'trips'
        ordering = ['-created_at']

class TripImage(models.Model):
    """
    Additional images for trips
    OOP Concept: Composition - Trip has multiple images
    """
    trip = models.ForeignKey(
        Trip, 
        on_delete=models.CASCADE,
        related_name='images'  # Access: trip.images.all()
    )
    image = models.ImageField(upload_to='trip_images/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.trip.title}"
    
    class Meta:
        ordering = ['uploaded_at']