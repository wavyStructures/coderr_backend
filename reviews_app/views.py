from django.shortcuts import render
from rest_framework.settings import api_settings
from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsReviewerOrReadOnly, IsCustomerAndAuthenticated

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    search_fields = ['description']
    ordering_fields = ['rating', 'updated_at']  
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomerAndAuthenticated()]
        return [permissions.IsAuthenticated()]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewerOrReadOnly]

