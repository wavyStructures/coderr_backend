from django.urls import path, include
from .views import BaseInfoView
from offers_app.api.views import OfferDetailsView
from orders_app.api.views import order_count, completed_order_count


urlpatterns = [
    path('', include('user_auth_app.api.urls')),
    path('profile/', include('profile_app.api.detail_urls')), 
    path('profiles/', include('profile_app.api.list_urls')),   
    
    path('offers/', include('offers_app.api.urls')),
    path('offerdetails/<int:pk>/', OfferDetailsView.as_view(), name='offer-details-view'), 
    
    path('order-count/<int:business_user_id>/', order_count, name='order-count'),
    path('completed-order-count/<int:business_user_id>/', completed_order_count, name='completed-order'),
    path('orders/', include('orders_app.api.urls')),
    
    path('reviews/', include('reviews_app.api.urls')),
    
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
]





