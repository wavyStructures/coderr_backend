from django.db import models
# from django.contrib.auth import get_user_model
from django.conf import settings
from offers_app.models import Offer
from django.utils.timezone import now

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    # customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    

    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', limit_choices_to={'type': 'customer'})
    business_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_orders', null=True, blank=True, limit_choices_to={'type': 'business'})

    order_id = models.AutoField(primary_key=True, default=333)
    
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)

    order_date = models.DateTimeField(default=now)
    
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_date = models.DateTimeField(null=True, blank=True)
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
    
    