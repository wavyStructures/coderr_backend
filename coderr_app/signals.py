from django.db.models.signals import post_migrate
from django.dispatch import receiver
from profile_app.models import Profile
from offers_app.models import Offer
from orders_app.models import Order
from reviews_app.models import Review
from django.contrib.auth.models import get_user_model


User = get_user_model()

@receiver(post_migrate)
def create_sample_data(sender, **kwargs):
    if sender.name == 'coderr_app':
        if not Profile.objects.exists():
            
            
            
            #my logic
            
            
            
            
            
            
            
            print("Creating dummy data")
            
            

