from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    Why: Converts Python objects to JSON and vice versa
    What: Handles data validation and transformation for API
    """
    
    # Custom field - not in model but calculated
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'phone', 'bio', 'avatar', 'date_of_birth'
        ]
        # Hide sensitive fields in API responses
        extra_kwargs = {
            'email': {'write_only': True},
        }
    
    def get_full_name(self, obj):
        """
        Custom method to get full name
        Why: Demonstrates SerializerMethodField usage
        """
        return obj.get_full_name()

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Separate serializer for user creation
    Why: Different validation rules for creation vs updates
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone'
        ]
    
    def validate(self, attrs):
        """
        Custom validation method
        Why: Ensures passwords match before creating user
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        """
        Custom create method
        Why: Properly hash password and remove confirm field
        """
        # Remove password_confirm as it's not needed for creation
        validated_data.pop('password_confirm')
        
        # Create user with hashed password
        user = User.objects.create_user(**validated_data)
        return user