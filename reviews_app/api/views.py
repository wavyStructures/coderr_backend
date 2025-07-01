from django.shortcuts import render
from rest_framework.settings import api_settings
from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Review
from .serializers import ReviewSerializer
from .permissions import IsReviewerOrReadOnly, IsCustomerAndAuthenticated


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    search_fields = ['description']
    ordering_fields = ['rating', 'updated_at']  
    
    def get_queryset(self):
        """
        Override the default get_queryset to filter the reviews based on the 'business_user_id' and 'reviewer_id' query parameters.

        Returns a queryset of Review objects filtered by the 'business_user_id' and 'reviewer_id' query parameters if they exist, otherwise returns all Review
        objects.
        """
        queryset = Review.objects.all()
        business_user_id = self.request.query_params.get('business_user_id')
        reviewer_id = self.request.query_params.get('reviewer_id')
    
        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        return queryset
    
    def perform_create(self, serializer):
        """
        Save the new review instance with the authenticated user as the reviewer.
        """
        serializer.save(reviewer=self.request.user)

    def get_permissions(self):
        """
        Override the default get_permissions method to return the appropriate permission classes for the request method.
        """
        
        if self.request.method == 'POST':
            return [IsCustomerAndAuthenticated()]
        return [permissions.IsAuthenticated()]


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewerOrReadOnly]

