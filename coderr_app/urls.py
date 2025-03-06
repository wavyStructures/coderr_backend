from django.urls import path, include

urlpatterns = [
    path('registration/', include('user_auth_app.urls')),
    path('login/', include('user_auth_app.urls')),
    
    path('profiles/', include('profile_app.urls')),
    
    path('offers/', include('offers_app.urls')),
    
    path('orders/', include('orders_app.urls')),
    
    path('reviews/', include('reviews_app.urls')),
    
    # path('base-info/', include('base_app.urls')),  
]