from django.db import models
from django.utils.timezone import now
from django.conf import settings


class Offer(models.Model):
    """
    Represents an offer created by a business user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offer')
    title = models.CharField(max_length=200, default="sample title")
    image = models.ImageField(upload_to="offers/", null=True, blank=True, default=None)
    description = models.TextField(default="sample description")
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    min_delivery_time = models.PositiveIntegerField(default=3)  

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    """
    Represents additional details for an offer.
    """

    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey("Offer", on_delete=models.CASCADE, related_name='details')
    description = models.TextField(default="sample description")
    title = models.CharField(max_length=200, default="sample title")
    revisions = models.PositiveIntegerField(default=0)
    delivery_time = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(default=list)  
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    class Meta:
        """
        Ensures there's only one basic, standard, and premium per offer.
        """

        unique_together = ('offer', 'offer_type')

    def __str__(self):
        return f"Detail for {self.offer.title} - {self.offer_type.capitalize()}"



    

