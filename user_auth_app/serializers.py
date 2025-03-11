from rest_framework import serializers
from user_auth_app.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture'] 
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']  
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False}  # Make email optional
        }  

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Ensures password is hashed
        user.save()
        return user
