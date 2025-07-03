from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from orders_app.models import Order
from offers_app.models import Offer
from .serializers import OrderSerializer, OrderCreateSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404


class OrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Retrieve the list of orders for the authenticated user.
        """
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"details": "Zugriff verweigert: Der Benutzer muss authentifiziert sein."},
                status=status.HTTP_401_UNAUTHORIZED
            )             
        
        try:
            user = request.user       
            orders = (
                Order.objects.filter(customer_user=user) |
                Order.objects.filter(business_user=user)
            )
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"details": "Interner Serverfehler.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """
        Create a new order for a customer.
        """
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"message": "Benutzer ist nicht authentifiziert."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if request.user.type != 'customer':
            return Response(
                {"message": "Benutzer hat keine Berechtigung, eine Bestellung zu erstellen (nur 'customer'-Benutzer erlaubt)."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OrderCreateSerializer(data=request.data, context={'request': request})

        if not request.data.get('offer_detail_id'):
            return Response(
                {"message": "Ungültige Anfragedaten: 'offer_detail_id' fehlt."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            try:
                order = serializer.save()
                response_serializer = OrderSerializer(order)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except OfferDetail.DoesNotExist:
                return Response(
                    {"message": "Das angegebene Angebotsdetail wurde nicht gefunden."},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"message": f"Interner Serverfehler: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {
                    "message": "Ungültige Anfragedaten.",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        """
        Partially update an existing order. 
        Accepts a JSON payload with the following attributes:status (string): One of the values in `Order.STATUS_CHOICES`
        """
        try:
            if not request.user or not request.user.is_authenticated:
                return Response(
                    {"message": "Benutzer ist nicht authentifiziert."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            order = get_object_or_404(Order, pk=pk)
            if request.user != order.business_user:
                return Response(
                    {"message": "Benutzer hat keine Berechtigung, diese Bestellung zu aktualisieren."},
                    status=status.HTTP_403_FORBIDDEN
                )

            new_status = request.data.get('status')
            if not new_status or new_status not in dict(Order.STATUS_CHOICES):
                return Response(
                    {"message": "Ungültiger Statuswert."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order.status = new_status
            order.save()

            order = get_object_or_404(Order, pk=pk)
            if request.user != order.business_user:
                raise PermissionDenied("Nur der Anbieter darf den Bestellstatus aktualisieren.")

            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                updated_order = serializer.save()
                return Response(
                    OrderSerializer(updated_order).data,
                    status=status.HTTP_200_OK
                )

        except Http404:
            return Response(
                {"message": "Die angegebene Bestellung wurde nicht gefunden."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": "Interner Serverfehler.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            
    def delete(self, request, pk):
        """
        Delete an order based on the provided primary key (pk).
        """
        try:
            if not request.user or not request.user.is_authenticated:
                return Response(
                    {"message": "Benutzer ist nicht authentifiziert."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            order = get_object_or_404(Order, pk=pk)

            if not request.user.is_staff:
                return Response(
                    {"message": "Benutzer ist nicht berechtigt, diese Bestellung zu löschen."},
                    status=status.HTTP_403_FORBIDDEN
                )

            order.delete()
            return Response(
                {"message": "Die Bestellung wurde erfolgreich gelöscht."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Order.DoesNotExist:
            return Response(
                {"message": "Es wurde keine Bestellung mit der angegebenen ID gefunden."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": "Interner Serverfehler.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_count(request, business_user_id):
    """
    Retrieve the count of in progress orders for a specified business user.
    """
    try:
        target_user = User.objects.get(pk=business_user_id, type='business')
    except User.DoesNotExist:
        return Response({'error': 'Kein Geschäftsnutzer mit dieser ID gefunden.'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        count = Order.objects.filter(business_user=target_user, status='in_progress').count()
        return Response({'order_count': count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Interner Serverfehler.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def completed_order_count(request, business_user_id):
    """
    Retrieve the count of completed orders for a specified business user.
    """
    try:
        user = User.objects.get(pk=business_user_id, type='business')
    except User.DoesNotExist:
        return Response({'error': 'Kein Geschäftsnutzer mit dieser ID gefunden.'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        count = Order.objects.filter(business_user=user, status='completed').count()
        return Response({'completed_order_count': count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Interner Serverfehler.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)