from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from reviews_app.models import Review
from offers_app.models import Offer
from user_auth_app.models import CustomUser
from django.shortcuts import render


class BaseInfoView(APIView):
    """
    API endpoint providing basic platform statistics such as number of reviews,
    average rating, number of business profiles, and number of offers.
    """

    def get(self, request):
        total_reviews = Review.objects.count()
        average_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']
        total_business_profiles = CustomUser.objects.filter(type='business').count()
        total_offers = Offer.objects.count()
        
        data = {
            "review_count": total_reviews,
            "average_rating": average_rating,
            "business_profile_count": total_business_profiles,
            "offer_count": total_offers
        }
        return Response(data)
    
    

    
    
    