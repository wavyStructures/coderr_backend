from django.apps import AppConfig
from django.conf import settings
from django.utils import timezone

from decimal import Decimal
import random
import sys


class ProfileAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile_app'
    
    def ready(self):
        # Avoid database operations during migration commands
        if "migrate" in sys.argv or "makemigrations" in sys.argv:
            return
    
        print("App is starting ... ensuring sample data exists.")
        
        
        # Move model imports here to avoid AppRegistryNotReady error
        from offers_app.models import Offer
        from offers_app.models import OfferDetail

        from orders_app.models import Order
        from reviews_app.models import Review
        from django.contrib.auth import get_user_model

        User = get_user_model()     
        
        self.create_sample_data(User, Offer, Order, OfferDetail, Review)

    def create_sample_data(self, User, Offer, Order, OfferDetail, Review):

                # Create or update customer users
        for i in range(5):
            user, created = User.objects.get_or_create(username=f'customer_user{i}')
            user.first_name = f'Customer{i}'
            user.last_name = f'LastNameC{i}'
            user.email = f'customer{i}@example.com'
            user.type = 'customer'
            
            # Only hash and set password if needed
            if not user.password or not user.password.startswith('pbkdf2_sha256$'):
                user.set_password('password123')
            
            user.save()
            print(f"{'Created' if created else 'Updated'} customer_user{i}")

        # Create or update business users
        for i in range(10):
            user, created = User.objects.get_or_create(username=f'business_user{i}')
            user.email = f'business{i}@example.com'
            user.first_name = f'Business{i}'
            user.last_name = f'LastNameB{i}'
            user.type = 'business'
            
            if not user.password or not user.password.startswith('pbkdf2_sha256$'):
                user.set_password('password123')
            
            user.save()
            print(f"{'Created' if created else 'Updated'} business_user{i}")

        # # Create or update customer users
        # for i in range(5):
        #     user, created = User.objects.update_or_create(
        #         username=f'customer_user{i}',
        #         defaults={
        #             'email': f'customer{i}@example.com',
        #             'password': 'password123',  # Use set_password for real passwords
        #             'type': 'customer',
        #         }
        #     )
        #     if created:
        #         print(f"Created customer_user{i}")
        #     else:
        #         print(f"Updated customer_user{i}")

        # # Create or update business users
        # for i in range(10):
        #     user, created = User.objects.update_or_create(
        #         username=f'business_user{i}',
        #         defaults={
        #             'email': f'business{i}@example.com',
        #             'password': 'password123',
        #             'type': 'business',
        #         }
        #     )
        #     if created:
        #         print(f"Created business_user{i}")
        #     else:
        #         print(f"Updated business_user{i}")

        # Create sample offers
        business_users = User.objects.filter(type="business")
        if business_users.exists():
            some_user_instance = business_users.first()  # Get the first business user
        else:
            some_user_instance = None  # Handle this case appropriately, maybe create a default user?

        OfferDetail.objects.all().delete()

        for i in range(10):
            offer, created = Offer.objects.update_or_create(
                title=f"Offer {i}",
                defaults={
                    'description': f"Description for offer {i}",
                    'user': some_user_instance,
                    'image': None,
                }
            )

            # Clear any existing offer details
            offer.details.all().delete()

            prices = []
            delivery_times = []


            offer_types = ['basic', 'standard', 'premium']
            for j, offer_type in enumerate(offer_types):  # Create 3 details per offer
                price = random.randint(50, 200)
                delivery_time = random.randint(1, 14)

                OfferDetail.objects.create(
                    offer=offer,
                    offer_type=offer_type,
                    price=price,
                    delivery_time=delivery_time,
                    title=f"{offer_type.capitalize()} Package",
                    description=f"Detail{j+1} for offer{i}"
                )

                prices.append(price)
                delivery_times.append(delivery_time)

            # Set the new annotated fields
            offer.min_price = min(prices)
            offer.min_delivery_time = min(delivery_times)
            offer.save()

            print(f"{'Created' if created else 'Updated'} Offer {i}")

        # Create sample orders       
        for i in range(5):
            Order.objects.update_or_create(
                order_id=i + 1,  
                defaults={
                    'customer_user': User.objects.filter(type='customer').order_by('?').first(),
                    'business_user': User.objects.filter(type='business').order_by('?').first(),
                    'offer': Offer.objects.order_by('?').first(),  
                    'status': random.choice(['pending', 'completed', 'in_progress']),
                    'price': offer.price if hasattr(offer, 'price') else Decimal('100.00'),
                    'order_date': timezone.now(),
                    'delivery_date': timezone.now() + timezone.timedelta(days=7),  
                }
            )
            print(f"Created/Updated Order {i + 1}")

        # Create sample reviews
        for i in range(10):
            Review.objects.update_or_create(
                id=i + 1,  
                defaults={
                    'customer': User.objects.filter(type='customer').order_by('?').first(),  
                    'offer': Offer.objects.order_by('?').first(),
                    'rating': random.randint(1, 5),
                    'comment': f"This is a review comment for review {i+1}.",
                }
            )
            print(f"Created/Updated Review {i + 1}")

        print("Sample data ensured.")