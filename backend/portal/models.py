from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model for the portal.
    Uses email as the primary login field.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    
    # Email verification
    is_email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    
    # Password reset
    reset_token = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Use email for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email