from django.contrib.auth.models import AbstractUser  # type: ignore
from django.db import models  # type: ignore

class User(AbstractUser):
 
    email = models.EmailField(unique=True)  # Email must be unique
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Set once when created
    updated_at = models.DateTimeField(auto_now=True)      # Updated every save
    
    # OOP Concept: Method overriding
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    class Meta:
        """
        Meta class provides metadata about the model
        Why: Helps Django understand how to handle the model
        """
        db_table = 'users'  # Custom table name
        verbose_name = 'User'
        verbose_name_plural = 'Users'