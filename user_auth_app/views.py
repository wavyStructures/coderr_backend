from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from orders_app.models import Order
from reviews_app.models import Review
from user_auth_app.serializers import CustomUserSerializer, RegisterSerializer


CustomUser = settings.AUTH_USER_MODEL
       
class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response({
            "username": "",
            "email": "",
            "password": ""
        })

    def post(self, request, *args, **kwargs):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                custom_user = serializer.save()
                token, created = Token.objects.get_or_create(user=custom_user)
                return Response({
                    "token": token.key,
                    "username": custom_user.username,
                    "email": custom_user.email,
                    "user_id": custom_user.id
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
       
class CheckUsernameView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        exists = User.objects.filter(username=username).exists()
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
 
        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,  
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }, status=status.HTTP_200_OK)
        








