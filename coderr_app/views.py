from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render


class BaseInfoView(APIView):
    """
    API endpoint providing basic platform statistics such as number of reviews,
    average rating, number of business profiles, and number of offers.
    """

    def get(self, request):
        data = {
            "total_reviews": 120,
            "average_rating": 4.5,
            "total_business_profiles": 50,
            "total_offers": 200
        }
        return Response(data)
    
    

    
    
    