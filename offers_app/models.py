from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model


# Create your models here.
class Offer(models.Model):
    """

    offer that a customer_user creates
    
    """
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='offer') 
    title = models.CharField(max_length=200)
    # image 
    description = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.title

