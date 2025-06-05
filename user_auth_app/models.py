from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, tel="123456789", **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, tel=tel, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, tel="123456789", **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, tel, **extra_fields)

class CustomUser(AbstractUser):
    TYPE_CHOICES = [
        ('customer', 'Kunde'),
        ('business', 'Anbieter'),
    ]
    
    username = models.CharField(
        max_length=80,
        unique=True,
        validators=[RegexValidator(
            regex=r"^[\w.@+\- ]+$",  
            message="Enter a valid username. Only letters, numbers, spaces, and @/./+/-/_ are allowed.",
            code="invalid"
        )]
    )
    file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)  
    
    
    uploaded_at = models.DateTimeField(null=True, blank=True) 
    location = models.CharField(max_length=100, null=True, blank=True, default="")
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=20, default="123456789")
    user_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='customer')
    
    description = models.TextField(blank=True, null=True)

    working_hours = models.CharField(max_length=80, null=True, blank=True, default="")
    created_at = models.DateTimeField(default=now)
    
    is_guest = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()  

    def save(self, *args, **kwargs):
        # if self.pk:
        #     original = CustomUser.objects  

        if self.file and not self.uploaded_at:
            self.uploaded_at = now()

        # if self.username == "guest":
        #     self.set_unusable_password()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

