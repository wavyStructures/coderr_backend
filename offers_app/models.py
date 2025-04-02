from django.db import models
from django.utils.timezone import now
from django.conf import settings

class Offer(models.Model):
    """
    Represents an offer created by a business user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offer')

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="offers/", null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_delivery_time = models.PositiveIntegerField()

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
    # offer = models.ForeignKey(on_delete=models.CASCADE, related_name='details', to=Offer)
    business = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    delivery_time = models.PositiveIntegerField(default=30)

    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)


    def __str__(self):
        return f"Detail for {self.offer.title}"