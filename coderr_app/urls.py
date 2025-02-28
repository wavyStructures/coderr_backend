from django.urls import path, include
from auth_app.views import LoginView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
]
