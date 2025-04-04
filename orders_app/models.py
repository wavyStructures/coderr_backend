from django.db import models
# from django.contrib.auth import get_user_model
from offers_app.models import Offer
from django.conf import settings

class Order(models.Model):
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    # customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', limit_choices_to={'type': 'customer'})
    business = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_orders')

    order_id = models.AutoField(primary_key=True)
    
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)  
    order_date = models.DateTimeField(auto_now_add=True)  
    delivery_date = models.DateTimeField(null=True, blank=True)  
