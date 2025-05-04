from django.db import models
from offers_app.models import Offer
from orders_app.models import Order
from django.conf import settings
from django.contrib.auth import get_user_model

CustomUser  = get_user_model()

class Review(models.Model):
    # customer = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE, limit_choices_to={'role': 'business'})
    # offer = models.ForeignKey(Offer, related_name='reviews', on_delete=models.CASCADE)
    # order = models.ForeignKey(Order, related_name='reviews', on_delete=models.CASCADE)
    # order = models.ForeignKey(Order, related_name='reviews', null=True, blank=True, on_delete=models.SET_NULL)

    # rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
   
    business_user = models.ForeignKey(
        CustomUser, related_name='received_reviews',
        on_delete=models.CASCADE, limit_choices_to={'role': 'business'}
    )
    reviewer = models.ForeignKey(
        CustomUser, related_name='written_reviews',
        on_delete=models.CASCADE, limit_choices_to={'role': 'customer'}
    )
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')