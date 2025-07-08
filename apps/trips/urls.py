from django.urls import path
from . import views

urlpatterns = [
    # Trip CRUD operations
    path('', views.TripListView.as_view(), name='trip-list'),
    path('create/', views.TripCreateView.as_view(), name='trip-create'),
    path('<int:pk>/', views.TripDetailView.as_view(), name='trip-detail'),
    path('<int:pk>/update/', views.TripUpdateView.as_view(), name='trip-update'),
    
    # User's trips
    path('my-trips/', views.UserTripsView.as_view(), name='user-trips'),
    
    # Trip images
    path('<int:trip_id>/upload-image/', views.upload_trip_image, name='upload-trip-image'),
]