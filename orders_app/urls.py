from django.urls import path
from .views import OrderListCreateAPIView, OrderStatusUpdateAPIView, OrderDeleteAPIView, order_count, completed_order_count

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderStatusUpdateAPIView.as_view(), name='order-update-status'),
    path('orders/<int:pk>/delete/', OrderDeleteAPIView.as_view(), name='order-delete'),
    path('order-count/<int:business_user_id>/', order_count, name='order-count'),
    path('completed-order-count/<int:business_user_id>/', completed_order_count, name='completed-order')
]


