from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer
from django.db.models import Min

class StandardResultsSetPagination(PageNumberPagination):
    # page_size = 10  
    page_size_query_param = "page_size"
    max_page_size = 100

class OfferListView(ListCreateAPIView):
    # queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = [
            'user',
        ]
    ordering_fields = [
            'created_at',
            'updated_at',
            'user',
        ]
    search_fields = ['title', 'description']

    def get_queryset(self):
        qs = Offer.objects.annotate(
            annotated_min_price=Min('details__price'),
            annotated_min_delivery_time=Min('details__delivery_time')
        )

        # Handle ?creator_id=2
        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            qs = qs.filter(user__id=creator_id)

        # Optional: filter for max_delivery_time
        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                qs = qs.filter(min_delivery_time__lte=int(max_delivery_time))
            except ValueError:
                pass

        # Manually filter by user__user_type
        user_type = self.request.query_params.get('user_type')
        if user_type:
            qs = qs.filter(user__user_type=user_type)

         # ✅ Filter by user__profile__location (assuming a OneToOne Profile model)
        location = self.request.query_params.get('location')
        if location:
            qs = qs.filter(user__profile__location__icontains=location)
        
        return qs


class OfferDetailView(RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    

