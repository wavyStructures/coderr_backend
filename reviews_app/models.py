from django.db import models
from django.contrib.auth import get_user_model
from offers_app.models import Offer
from orders_app.models import Order


# Review Model (for customers to review an order/offer)
class Review(models.Model):
    customer = models.ForeignKey(get_user_model(), related_name='reviews', on_delete=models.CASCADE, limit_choices_to={'role': 'business'})
    offer = models.ForeignKey(Offer, related_name='reviews', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

