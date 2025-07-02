from django.db import transaction
from django.db.models import Min
from django.http import Http404

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.exceptions import PermissionDenied, ValidationError, NotAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from ..models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer, PublicOfferSerializer, OfferSingleSerializer

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
            'min_price',
            'min_delivery_time',
        ]
    search_fields = ['title', 'description']
    
    
    def get_permissions(self):
        """
        Override the default `get_permissions` method to allow any request when the request method is GET. 
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


    def get_queryset(self):
        """
        Retrieve a queryset of offers with annotated minimum price and delivery time.
        """
        try:
            qs = Offer.objects.annotate(
                annotated_min_price=Min('details__price'),
                annotated_min_delivery_time=Min('details__delivery_time_in_days')
            )

            min_price = self.request.query_params.get('min_price')
            if min_price:
                min_price = float(min_price)
                qs = qs.filter(annotated_min_price__gte=min_price)

            creator_id = self.request.query_params.get('creator_id')
            if creator_id:
                qs = qs.filter(user__id=creator_id)

            min_delivery_time = self.request.query_params.get('min_delivery_time')
            if min_delivery_time:
                min_delivery_time = int(min_delivery_time)
                qs = qs.filter(annotated_min_delivery_time__gte=min_delivery_time)
                        
            max_delivery_time = self.request.query_params.get('max_delivery_time')
            if max_delivery_time:
                max_delivery_time = int(max_delivery_time)
                qs = qs.filter(annotated_min_delivery_time__lte=max_delivery_time)

            type = self.request.query_params.get('type')
            if type:
                qs = qs.filter(user__type=type)

            location = self.request.query_params.get('location')
            if location:
                qs = qs.filter(user__profile__location__icontains=location)
            return qs

        except (ValueError, TypeError) as e:
            raise ValidationError({'detail': 'Ungültige Anfrageparameter.', 'error': str(e)})

    def get_serializer_class(self):
        """
        Choose the appropriate serializer class for the request method. Method GET > OfferSerializer, otherwise > PublicOfferSerializer.
        """
        if self.request.method == "GET":
            return OfferSerializer
        return PublicOfferSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new offer with the given details. The authenticated user must be of type 'business' to create an offer.
        """
        user = request.user

        if not user or not user.is_authenticated:
            return Response({'message': 'Benutzer ist nicht authentifiziert.'}, status=status.HTTP_401_UNAUTHORIZED)

        if getattr(user, 'type', None) != 'business':
            return Response({'message': "Authentifizierter Benutzer ist kein 'business' Profil."}, status=status.HTTP_403_FORBIDDEN)

        try:
            response = super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'message': 'Ungültige Anfragedaten oder unvollständige Details.', 'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Interner Serverfehler beim Erstellen des Angebots.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        offer_id = response.data.get('id')
        if not offer_id:
            return response

        try:
            full_offer = Offer.objects.get(pk=offer_id)
            public_data = PublicOfferSerializer(full_offer, context=self.get_serializer_context()).data
            return Response(public_data, status=status.HTTP_201_CREATED)
        except Offer.DoesNotExist:
            return Response({'message': 'Angebot wurde erstellt, aber konnte nicht geladen werden.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Interner Serverfehler nach der Angebotserstellung.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class OfferDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class OfferDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        """
        Determine the permissions for the current request.
        """
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve an offer detail by its ID.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            response = Response(serializer.data, status=status.HTTP_200_OK)
            response['X-Status-Message'] = 'Das Angebotsdetail wurde erfolgreich abgerufen.'
            return response

        except Http404: 
            return Response(
                {'message': 'Das Angebotsdetail mit der angegebenen ID wurde nicht gefunden.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionDenied as e:
            return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {'message': 'Interner Serverfehler beim Laden des Angebotsdetails.', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class OfferSingleView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()

    def get_serializer_class(self):
        """
        Choose the appropriate serializer class for the request method. Method GET > OfferSingleSerializer, otherwise > PublicOfferSerializer.
        """
        if self.request.method == "GET":
            return OfferSingleSerializer
        return PublicOfferSerializer

    def get_permissions(self):
        """
        Determine the permissions for the current request.

        For GET requests, everyone is allowed to retrieve the offer. All other
        methods, only the owner of the offer is allowed to perform the action.
        """
        return [IsAuthenticated(), IsOwnerOrReadOnly()]
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Benutzer ist nicht authentifiziert"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = self.get_serializer(data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                {"message": "Ungültige Anfragedaten oder unvollständige Details.", "errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )  
            
        try:
            instance = self.get_object()
        except Http404:
            return Response(
                {"message": "Das Angebot mit der angegebenen ID wurde nicht gefunden."},
                status=status.HTTP_404_NOT_FOUND
            )

        if instance.owner != request.user:
            return Response(
                {"message": "Authentifizierter Benutzer ist nicht der Eigentümer des Angebots"},
                status=status.HTTP_403_FORBIDDEN
            )
      
        serializer = self.get_serializer(data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                {"message": "Ungültige Anfragedaten oder unvollständige Details.", "errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"message": "Das Angebot wurde erfolgreich aktualisiert.", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        """
        Retrieve the queryset of offers with annotated minimum price and delivery time.
        """
        return Offer.objects.annotate(
            annotated_min_price=Min('details__price'),
            annotated_min_delivery_time=Min('details__delivery_time_in_days')
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve an offer by its ID.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            return response
        
        except Http404:
            return Response({'message': 'Das Angebot mit der angegebenen ID wurde nicht gefunden.'},
                        status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'message': 'Authentifizierter Benutzer ist nicht der Eigentümer des Angebots.'}, 
                            status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'message': 'Interner Serverfehler beim Laden des Angebots.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes the offer with the given ID if the authenticated user is the owner of the offer.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response({'message': 'Das Angebot wurde nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'message': 'Authentifizierter Benutzer ist nicht der Eigentümer des Angebots.'}, 
                            status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'message': 'Interner Serverfehler beim Löschen des Angebots.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            