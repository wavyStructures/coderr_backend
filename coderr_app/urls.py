from django.urls import path, include
from .views import BaseInfoView
from offers_app.views import OfferDetailsView
from orders_app.views import order_count, completed_order_count


urlpatterns = [
    path('', include('user_auth_app.urls')),
    path('profile/', include('profile_app.detail_urls')), 
    path('profiles/', include('profile_app.list_urls')),   
    
    path('offers/', include('offers_app.urls')),
    path('offerdetails/<int:pk>/', OfferDetailsView.as_view(), name='offer-details-view'), 
    
    path('order-count/<int:business_user_id>/', order_count, name='order-count'),
    path('completed-order-count/<int:business_user_id>/', completed_order_count, name='completed-order'),
    path('orders/', include('orders_app.urls')),
    
    path('reviews/', include('reviews_app.urls')),
    
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
]




