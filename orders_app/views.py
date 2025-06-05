from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from orders_app.models import Order
from offers_app.models import Offer
from .serializers import OrderSerializer, OrderCreateSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404

class OrderListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})

        if request.user.type != 'customer':
            raise PermissionDenied("Only customers can place orders.")
        if serializer.is_valid():
            order = serializer.save()
            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if request.user != order.business_user:
            raise PermissionDenied("Only business users can update order status")
        
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, pk):
        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can delete orders.")

        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


    
    
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def order_count(request, business_user_id):
    try:
        user = User.objects.get(pk=business_user_id, user_type='business')
    except User.DoesNotExist:
        return Response({'error':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    count = Order.objects.filter(business_user=user, status='in_progress').count()
    return Response({'order_count': count})


@api_view(['GET'])
@permission_classes([AllowAny])
def completed_order_count(request, business_user_id):
    user = get_object_or_404(User, pk=business_user_id, user_type='business')
    count = Order.objects.filter(business_user=user, status='completed').count()
    return Response({'completed_order_count': count})

