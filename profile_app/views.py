from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from user_auth_app.models import CustomUser
from user_auth_app.serializers import CustomUserSerializer 


class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, pk):
        return get_object_or_404(CustomUser, pk=pk)
          

    def get(self, request, pk):
        try:
            user = self.get_object(pk)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            user = self.get_object(pk)
            
            if request.user != user:
                return Response({"error": "You do not have permission to edit this profile."}, status=status.HTTP_403_FORBIDDEN)

            serializer = CustomUserSerializer(user, data=filtered_data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except NotFound:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An expected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        try: 
            user = self.get_object(pk)
        
            if request.user != user and not request.user.is_superuser:
                return Response({"error": "You do not have permission to delete this profile."}, status=status.HTTP_403_FORBIDDEN)

            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except NotFound:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customers = CustomUser.objects.filter(type="customer")
        serializer = CustomUserSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusinessListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        businesses = CustomUser.objects.filter(type="business")
        serializer = CustomUserSerializer(businesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)