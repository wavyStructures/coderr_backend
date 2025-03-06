from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from user_auth_app.models import CustomUser
from user_auth_app.serializers import CustomUserSerializer, RegisterSerializer

from django.contrib.auth import get_user_model

User = get_user_model() 
       
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
                    "user": {
                        "username": custom_user.username,
                        "email": custom_user.email,
                        "password": custom_user.password,
                    },
                    "token": token.key,
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
        # return Response({'exists': exists})
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

        if username == "guest" and password == "guestpassword":
            guest_user = User.objects.filter(username="guest").first()
            if not guest_user:
                guest_user = User.objects.create_user(username="guest", password="guestpassword", is_guest=True)
            token, created = Token.objects.get_or_create(user=guest_user)
            return Response({
                "user": {
                    "id": guest_user.id,
                    "username": guest_user.username,
                    "email": guest_user.email,
                },
                "token": token.key,
            }, status=status.HTTP_200_OK)

        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        
        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                # "phone": user.phone,
            },
            "token": token.key,  
        }, status=status.HTTP_200_OK)
        








