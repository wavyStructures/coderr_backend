from django.db import models
from django.conf import settings
from offers_app.models import Offer
from django.utils.timezone import now
from django.core.validators import MinValueValidator

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
 
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', limit_choices_to={'user_type': 'customer'})
    business_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_orders', null=True, blank=True, limit_choices_to={'user_type': 'business'})
 
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(default=now)
    
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0,  validators=[MinValueValidator(-1)],
    help_text="-1 for unlimited")    
    delivery_time_in_days = models.PositiveIntegerField(default=7)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    