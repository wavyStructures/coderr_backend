import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from profile_app.models import Profile
from offers_app.models import Offer
from orders_app.models import Order
from reviews_app.models import Review
from coderr_app.models import BaseInfo

User = get_user_model()

class Command(BaseCommand):
    help = "Populate the database with sample data."

    def handle(self, *args, **kwargs):
        # Create sample users
        for i in range(5):
            user = User.objects.create_user(
                username=f"business_user{i}",
                email=f"business_user{i}@gmx.de",
                password=f"business_user{i}",
            )
            Profile.objects.create(user=user, type='business')
        
            user = User.objects.create_user(
                username=f"customer_user{i}",
                email=f"customer_user{i}@gmx.de",
                password=f"customer_user{i}",
            )
            Profile.objects.create(user=user, type='customer')    
        
        # Create sample offers
        for i in range(10):
            Offer.objects.create(
                title=f"Offer{i}",
                 description=f'This is a test offer {i}',
                price=random.randint(10, 500),
                business=Profile.objects.filter(role='business').order_by('?').first(),
            )

        # Create Orders
        for i in range(5):
            Order.objects.create(
                customer=Profile.objects.filter(role='customer').order_by('?').first(),
                offer=Offer.objects.order_by('?').first(),
                status=random.choice(['pending', 'completed'])
            )

        # Create Reviews
        for i in range(5):
            Review.objects.create(
                user=User.objects.order_by('?').first(),
                rating=random.randint(1, 5),
                comment=f'Test review {i}',
            )

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))