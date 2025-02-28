from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
        TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True)   
    file = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)    #Pillow installed (pip install pillow) for image handling.
    location = models.CharField(max_length=55, null=True, blank=True, default="")
    tel = models.CharField(max_length=20, null=True, blank=True, default="")
    description = models.TextField(null=True, blank=True, default="")
    working_hours = models.CharField(max_length=50, null=True, blank=True, default="")
    type = models.CharField(max_length=50, choices=[('business', 'Business'), ('personal', 'Personal')], default='personal')
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    
    
    
    
    
    
    