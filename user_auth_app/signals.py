# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from coderr.models import Offer, Order, Review
# from django.conf import settings

# CustomUser = settings.AUTH_USER_MODEL

# @receiver(post_save, sender=User)
# def create_sample_data_for_new_user(sender, instance, created, **kwargs):
#     """
#     Automatically generate dummy data when a new user is created.
#     - Business users get 2 sample offers.
#     - Customer users get 1 sample order + reviews.
#     """
#     if created:
#         if instance.role == "business":
#             Offer.objects.create(
#                 user=instance,
#                 title=f"Sample Offer 1 by {instance.username}",
#                 description="auto-generated offer1."
#             )
#             Offer.objects.create(
#                 user=instance,
#                 title=f"Sample Offer 2 by {instance.username}",
#                 description="auto-generated offer2."
#             )
#         elif instance.role == "customer":
#             sample_order = Order.objects.create(
#                 customer=instance,
#                 offer=Offer.objects.order_by("?").first(),
#                 status="pending"    
#             )
#             Review.objects.create(
#                 order=sample_order,
#                 rating=4,
#                 comment="This is a sample review."
#             )
            
