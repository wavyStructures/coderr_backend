from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         # fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture'] 
#         fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", 
            "username", 
            "first_name", 
            "last_name", 
            "file",
            "location",
            "tel", 
            "description",
            "working_hours",
            "type",  
            "email",
            "created_at"
        ]
                
        read_only_fields = ["id", "username", "email", "is_active"]  # Prevent users from modifying these

    def update(self, instance, validated_data):

        allowed_fields = {"first_name", "last_name", "tel", "file"}
        for field in list(validated_data.keys()):
            if field not in allowed_fields:
                validated_data.pop(field)

        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True, required=True) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False}  # Make email optional
        }  

    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = CustomUser.objects.create_user(**validated_data)        

        return user
