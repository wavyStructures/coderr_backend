from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer
from django.db.models import Min

from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied


class StandardResultsSetPagination(PageNumberPagination):
    # page_size = 10  
    page_size_query_param = "page_size"
    max_page_size = 100

class OfferListView(APIView):
    def get(self, request):
        offers = Offer.objects.annotate(
            annotated_min_price=Min('details__price'),
            annotated_min_delivery_time=Min('details__delivery_time_in_days')
        )

        creator_id = request.query_params.get('creator_id')
        if creator_id:
            offers = offers.filter(user__id=creator_id)

        max_delivery_time = request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                offers = offers.filter(annotated_min_delivery_time__lte=int(max_delivery_time))
            except ValueError:
                pass

        user_type = request.query_params.get('user_type')
        if user_type:
            offers = offers.filter(user__user_type=user_type)

        location = request.query_params.get('location')
        if location:
            offers = offers.filter(user__profile__location__icontains=location)

        paginator = StandardResultsSetPagination()
        paginated_qs = paginator.paginate_queryset(offers, request)
        serializer = OfferSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        user = request.user

        print(user)
        print(user.user_type)

        if not user or not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        if user.user_type != 'business':
            raise PermissionDenied("Only business users can create offers.")

        data = request.data
        details = data.get("details", [])

        if not isinstance(details, list) or len(details) != 3:
            raise ValidationError("An offer must contain exactly 3 details.")

        try:
            with transaction.atomic():
                offer_data = {
                    "title": data.get("title"),
                    "description": data.get("description"),
                    "image": data.get("image"),
                    "user": user.id,
                }

                offer_serializer = OfferSerializer(data=offer_data)
                offer_serializer.is_valid(raise_exception=True)
                offer = offer_serializer.save()

                created_details = []
                for detail in details:
                    detail_data = {
                        "offer": offer.id,
                        "title": detail.get("title"),
                        "revisions": detail.get("revisions"),
                        "delivery_time_in_days": detail.get("delivery_time_in_days"),
                        "price": detail.get("price"),
                        "features": detail.get("features"),
                        "offer_type": detail.get("offer_type"),
                    }
                    detail_serializer = OfferDetailSerializer(data=detail_data)
                    detail_serializer.is_valid(raise_exception=True)
                    detail_serializer.save()
                    created_details.append(detail_serializer.data)

                response_data = offer_serializer.data
                response_data["details"] = created_details

                return Response(response_data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"detail": e.detail if hasattr(e, "detail") else str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Unexpected error:", e)
            return Response({"detail": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class OfferListView(ListCreateAPIView):
#     serializer_class = OfferSerializer
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

#     filterset_fields = [
#             'user',
#         ]
#     ordering_fields = [
#             'created_at',
#             'updated_at',
#             'user',
#         ]
#     search_fields = ['title', 'description']

#     def get_queryset(self):
#         qs = Offer.objects.annotate(
#             annotated_min_price=Min('details__price'),
#             annotated_min_delivery_time=Min('details__delivery_time_in_days')
#         )

#         creator_id = self.request.query_params.get('creator_id')
#         if creator_id:
#             qs = qs.filter(user__id=creator_id)

#         max_delivery_time = self.request.query_params.get('max_delivery_time')
#         if max_delivery_time:
#             try:
#                 qs = qs.filter(min_delivery_time__lte=int(max_delivery_time))
#             except ValueError:
#                 pass

#         user_type = self.request.query_params.get('user_type')
#         if user_type:
#             qs = qs.filter(user__user_type=user_type)

#         location = self.request.query_params.get('location')
#         if location:
#             qs = qs.filter(user__profile__location__icontains=location)
        
#         return qs

#     def perform_create(self, serializer):
#         user = self.request.user
#         if not user.is_authenticated:
#             raise PermissionDenied("Authentication required.")

#         if user.user_type != 'business':
#             raise PermissionDenied("Only business users can create offers.")

#         # details = serializer.validated_data.get("details")
#         details = self.request.data.get("details", [])
#         if not isinstance(details, list) or len(details) != 3:
#             raise ValidationError("An offer must contain exactly 3 details.")
#         serializer.save(user=user)
        
    # def post(self, request, *args, **kwargs):
    #     print("POST method called") 
    #     user = request.user

    #     if not user or not user.is_authenticated:
    #         return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    #     if getattr(user, "user_type", None) != 'business':
    #         return Response({"detail": "Only business users can create offers."}, status=status.HTTP_403_FORBIDDEN)

    #     data = request.data
    #     details = data.get("details", [])

    #     if not isinstance(details, list) or len(details) != 3:
    #         return Response({"detail": "An offer must contain exactly 3 details."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         with transaction.atomic():
    #             offer_data = {
    #                 "title": data.get("title"),
    #                 "description": data.get("description"),
    #                 "image": data.get("image"),
    #                 "user": user.id,  # assumes serializer accepts PK
    #             }

    #             offer_serializer = OfferSerializer(data=offer_data)
    #             offer_serializer.is_valid(raise_exception=True)
    #             offer = offer_serializer.save()

    #             created_details = []
    #             for detail in details:
    #                 detail_data = {
    #                     "offer": offer.id,
    #                     "title": detail.get("title"),
    #                     "revisions": detail.get("revisions"),
    #                     "delivery_time_in_days": detail.get("delivery_time_in_days"),
    #                     "price": detail.get("price"),
    #                     "features": detail.get("features"),
    #                     "offer_type": detail.get("offer_type"),
    #                 }
    #                 detail_serializer = OfferDetailSerializer(data=detail_data)
    #                 detail_serializer.is_valid(raise_exception=True)
    #                 created_detail = detail_serializer.save()
    #                 created_details.append(detail_serializer.data)

    #             response_data = offer_serializer.data
    #             response_data["details"] = created_details

    #             return Response(response_data, status=status.HTTP_201_CREATED)

    #     except ValidationError as e:
    #         return Response({"detail": e.detail if hasattr(e, "detail") else str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #     except Exception as e:
    #         print("Unexpected error:", e)
    #         return Response({"detail": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OfferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all().order_by('id')
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    

class OfferDetailRetrieveView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer


