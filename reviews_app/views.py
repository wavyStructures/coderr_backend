from django.shortcuts import render
from rest_framework import generics
from reviews_app.models import Review
from .serializers import ReviewSerializer

class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

