from django.urls import path
from . import views

urlpatterns = [
    # Booking operations
    path('create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('my-bookings/', views.UserBookingsView.as_view(), name='user-bookings'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    
    # Trip bookings (for trip creators)
    path('trip/<int:trip_id>/', views.TripBookingsView.as_view(), name='trip-bookings'),
    
    # Booking actions
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel-booking'),
    path('<int:booking_id>/confirm/', views.confirm_booking, name='confirm-booking'),
]