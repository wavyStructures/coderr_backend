from django.apps import AppConfig
from django.conf import settings
import random


class ProfileAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile_app'
    
    def ready(self):
        print("App is starting ... ensuring sample data exists.")
        
        
        # Move model imports here to avoid AppRegistryNotReady error
        from offers_app.models import Offer
        from orders_app.models import Order
        from reviews_app.models import Review
        from django.contrib.auth import get_user_model

        User = get_user_model()     
        
        self.create_sample_data(User, Offer, Order, Review)

    def create_sample_data(self, User, Offer, Order, Review):
        # Create or update customer users
        for i in range(5):
            user, created = User.objects.update_or_create(
                username=f'customer_user{i}',
                defaults={
                    'email': f'customer{i}@example.com',
                    'password': 'password123',  # Use set_password for real passwords
                    'type': 'customer',
                }
            )
            if created:
                print(f"Created customer_user{i}")
            else:
                print(f"Updated customer_user{i}")

        # Create or update business users
        for i in range(10):
            user, created = User.objects.update_or_create(
                username=f'business_user{i}',
                defaults={
                    'email': f'business{i}@example.com',
                    'password': 'password123',
                    'type': 'business',
                }
            )
            if created:
                print(f"Created business_user{i}")
            else:
                print(f"Updated business_user{i}")

        # Create sample offers
        business_users = User.objects.filter(type="business")
        if business_users.exists():
            some_user_instance = business_users.first()  # Get the first business user
        else:
            some_user_instance = None  # Handle this case appropriately, maybe create a default user?
        for i in range(10):
            offer, created = Offer.objects.update_or_create(
                title=f"Offer {i}",
                defaults={
                    'description': f"Description for offer {i}",
                    'user': some_user_instance,  # Assign the user here

                    # ,
                    # 'price': random.randint(50, 200)
                }
            )
            if created:
                print(f"Created Offer {i}")
            else:
                print(f"Updated Offer {i}")

        # Create sample orders       
        for i in range(5):
            Order.objects.update_or_create(
                order_id=i + 1,  
                defaults={
                    'user': User.objects.filter(type='customer').order_by('?').first(),  # Random customer
                    'offer': Offer.objects.order_by('?').first(),  # Random offer
                    'status': random.choice(['pending', 'completed', 'in_progress']),
                    'order_date': "2025-03-01",
                    'delivery_date': "2025-03-10",
                }
            )
            print(f"Created/Updated Order {i + 1}")

        # Create sample reviews
        for i in range(10):
            Review.objects.update_or_create(
                id=i + 1,  
                defaults={
                    'user': User.objects.filter(type='customer').order_by('?').first(),  # Random customer
                    'offer': Offer.objects.order_by('?').first(),  # Random offer
                    'rating': random.randint(1, 5),
                    'comment': f"This is a review comment for review {i}.",
                }
            )
            print(f"Created/Updated Review {i + 1}")

        print("Sample data ensured.")