from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('host', 'Host'),
        ('donor', 'Donor'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    email = models.EmailField(unique=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)  # Add this field
    is_active = models.BooleanField(default=False)

    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    company_website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    is_host = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_profile_complete = models.BooleanField(default=False)  # Track if user has completed profile

    def __str__(self):
        return self.user.username
