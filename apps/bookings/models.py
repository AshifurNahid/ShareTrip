from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from apps.trips.models import Trip

User = get_user_model()

class Booking(models.Model):
    """
    Booking model represents a user's trip booking
    OOP Concept: Association - connects User and Trip
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Foreign Key relationships
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    trip = models.ForeignKey(
        Trip, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_people = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.user.username} - {self.trip.title}"
    
    class Meta:
        db_table = 'bookings'
        unique_together = ['user', 'trip']
        ordering = ['-booking_date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'