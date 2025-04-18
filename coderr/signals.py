# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from profile_app.models import Profile
# from offers_app.models import Offer
# from orders_app.models import Order
# from reviews_app.models import Review
# from django.contrib.auth.models import get_user_model
# import random

# User = get_user_model()

# @receiver(post_migrate)
# def create_sample_data(sender, **kwargs):
#     if sender.name == 'coderr':

#         # if not User.objects.filter(username='customer_user0').exists():

#         # Fixed set of customer users (5)
#         print("Creating customer users...")
#         customer_users = [
#             User.objects.create_user(
#                 username='customer_user0',
#                 email='customer0@example.com',
#                 password='password123',
#                 type='customer'
#             ),
#             User.objects.create_user(
#                 username='customer_user1',
#                 email='customer1@example.com',
#                 password='password123',
#                 type='customer'
#             ),
#             User.objects.create_user(
#                 username='customer_user2',
#                 email='customer2@example.com',
#                 password='password123', 
#                 type='customer'
#             ),
#             User.objects.create_user(
#                 username='customer_user3',
#                 email='customer3@example.com',
#                 password='password123', 
#                 type='customer'
#             ),
#             User.objects.create_user(
#                 username='customer_user4',
#                 email='customer4@example.com',
#                 password='password123', 
#                 type='customer'
#             ),
#         ]
#         # else:
#         #     print("Customer users already exist, skipping...")


#         # if not User.objects.filter(username='business_user0').exists():
#         # Fixed set of business users (10)
#         print("Creating business users...")
#         business_users = [
#             User.objects.create_user(
#                 username=f'business_user{i}',
#                 email=f'business{i}@example.com',
#                 password='password123',
#                 type='business'
#             ) for i in range(10)
#         ]
#         # else:
#         #     print("Business users already exist, skipping...")


#         # Fixed set of offers (10)
#         print("Creating offers...")
#         offers = [
#             Offer.objects.create(
#                 title=f"Offer {i}",
#                 description=f"Description for offer {i}",
#                 price=random.randint(50, 200),  # Random price between 50 and 200
#                 available=True,
#             ) for i in range(10)
#         ]
       

#         # Fixed set of orders (5)
#         print("Creating orders...")
#         orders = [
#             Order.objects.create(
#                 user=random.choice(customer_users),  # Randomly pick a customer user
#                 offer=random.choice(offers),  # Randomly pick an offer
#                 status=random.choice(['pending', 'completed', 'in_progress']),
#                 order_date="2025-03-01",  # Fixed date
#                 delivery_date="2025-03-10",  # Fixed delivery date
#             ) for _ in range(5)
#         ]
        
#         # Fixed set of reviews (10)
#         print("Creating reviews...")
#         reviews = [
#             Review.objects.create(
#                 user=random.choice(customer_users),  # Randomly pick a customer user
#                 offer=random.choice(offers),  # Randomly pick an offer
#                 rating=random.randint(1, 5),  # Random rating between 1 and 5
#                 comment=f"This is a review comment for review {i}.",
#             ) for i in range(10)
#         ]
       

#         print("Dummy data creation complete!")
            

            
            

