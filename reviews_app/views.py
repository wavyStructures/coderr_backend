from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from reviews_app.models import Review
from .serializers import ReviewSerializer
from .permissions import IsReviewerOrReadOnly, IsCustomerAndAuthenticated

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    search_fields = ['description']
    ordering_fields = ['rating', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsCustomerAndAuthenticated]
        else:
            permission_classes = [IsReviewerOrReadOnly]
        return [permission() for permission in permission_classes]
    
    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [IsCustomerAndAuthenticated()]
    #     return [permissions.IsAuthenticated()]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewerOrReadOnly]