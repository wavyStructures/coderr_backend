from django.db import transaction
from django.db.models import Min
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer, PublicOfferSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6  
    page_size_query_param = "page_size"
    max_page_size = 100


class OfferListView(ListCreateAPIView):
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
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = Offer.objects.annotate(
            annotated_min_price=Min('details__price'),
            annotated_min_delivery_time=Min('details__delivery_time_in_days')
        )

        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            qs = qs.filter(user__id=creator_id)

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                qs = qs.filter(min_delivery_time__lte=int(max_delivery_time))
            except ValueError:
                pass

        user_type = self.request.query_params.get('user_type')
        if user_type:
            qs = qs.filter(user__user_type=user_type)

        location = self.request.query_params.get('location')
        if location:
            qs = qs.filter(user__profile__location__icontains=location)
        
        return qs
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferSerializer
        return PublicOfferSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        offer_id = response.data.get('id')
        if not offer_id:
            return response

        try:
            full_offer = Offer.objects.get(pk=offer_id)
        except Offer.DoesNotExist:
            return response
        
        public_data = PublicOfferSerializer(full_offer, context=self.get_serializer_context()).data
        return Response(public_data, status=status.HTTP_201_CREATED)

class OfferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all().order_by('id')
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    

class OfferDetailRetrieveView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer

