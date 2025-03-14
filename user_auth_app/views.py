from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from user_auth_app.serializers import CustomUserSerializer, RegisterSerializer
from django.contrib.auth import get_user_model
from offers_app.models import Offer
from orders_app.models import Order
from reviews_app.models import Review

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

        if username == ["demo_business", "demo_customer"] and password == "guestpassword":
            guest_user, created = User.objects.get_or_create(
                username=username, defaults={"password": "guestpassword", "role": "business" if "business" in username else "customer"}
            )
            
            # Delete old demo data for this guest user
            Offer.objects.filter(user=guest_user).delete()
            Order.objects.filter(customer=guest_user).delete()
            Review.objects.filter(order__customer=guest_user).delete()
            
            #Generate fresh demo data
            if username == "demo_business":
                Offer.objects.create(user=guest_user, title="Demo Offer 1", description="auto-generated description")
                Offer.objects.create(user=guest_user, title="Demo Offer 2", description="auto-generated description")
            elif username == "demo_customer":
                sample_order = Order.objects.create(customer=guest_user, offer=Offer.objects.order_by("?").first(), status="pending")
                Review.objects.create(order=sample_order, rating=5, comment="Great service!")
                
            #Create or get token
            token, _ = Token.objects.get_or_create(user=guest_user)
            return Response ({
                "user": {"id": guest_user.id, "username": guest_user.username, "role": guest_user.role},
                "token": token.key,
            }, status=200)
            
        #Regular user login
        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=400)
        
        user = User.objects.filter(username=username).first()
        
        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid username or password.'}, status=400)
            # return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)

        #Create or get token for regular users
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role},
            "token": token.key,
        }, status=200)
 






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
        








