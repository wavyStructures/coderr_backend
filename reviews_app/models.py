from django.db import models
from offers_app.models import Offer
from orders_app.models import Order
from django.conf import settings
from django.contrib.auth import get_user_model

CustomUser  = get_user_model()

class Review(models.Model):
   
    business_user = models.ForeignKey(
        CustomUser, related_name='received_reviews',
        on_delete=models.CASCADE, limit_choices_to={'type': 'business'}, 
        null=True
    )

    reviewer = models.ForeignKey(
        CustomUser, related_name='written_reviews',
        on_delete=models.CASCADE, limit_choices_to={'type': 'customer'},
        null=True
    )
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')
        
        
        

