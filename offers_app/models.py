from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

class Offer(models.Model):
    """
    Represents an offer created by a business user.
    """
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='offer') 
    title = models.CharField(max_length=200)
    # image 
    description = models.TextField()
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)
    min_price = models.FloatField()  
    min_delivery_time = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class OfferDetail(models.Model):
    """
    Represents additional details for an offer.
    """
    offer = models.ForeignKey(on_delete=models.CASCADE, related_name='details', to=Offer)
    
    url = models.URLField()  # Each detail will have a URL

    def __str__(self):
        return f"Detail for {self.offer.title}"