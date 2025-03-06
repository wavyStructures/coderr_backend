from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from user_auth_app.models import CustomUser
from user_auth_app.serializers import CustomUserSerializer 


class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return None  

    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        allowed_fields = {"first_name", "last_name", "phone_number", "profile_picture"}
        filtered_data = {key: value for key, value in request.data.items() if key in allowed_fields}

        serializer = CustomUserSerializer(user, data=filtered_data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 



class CustomerListView(APIView):
    pass

 
 
 
class BusinessListView(APIView):
    pass