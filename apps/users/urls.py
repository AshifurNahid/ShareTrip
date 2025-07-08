from django.urls import path
from . import views

urlpatterns = [
    # User authentication and profile
    path('register/', views.UserCreateView.as_view(), name='user-register'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('stats/', views.user_stats, name='user-stats'),
]