from rest_framework import serializers
from ..models import CustomUser 


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
                
        read_only_fields = ["id", "username", "email", "is_active"]   

    def update(self, instance, validated_data):
        """
        Updates a user instance with the given validated data.
        """    
        allowed_fields = {
            "first_name", "last_name", "tel", "file", 
            "location", "description", "working_hours"
        }
        
        for field in list(validated_data.keys()):
            if field not in allowed_fields:
                validated_data.pop(field)

        return super().update(instance, validated_data)


class FlattenedUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = CustomUser
        fields = [
            'user',  
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type'
        ]

    def get_user(self, obj):
        """
        Returns the user's id.
        """
        return obj.user.id 

    
class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True, required=True) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False}  
        }  

    def validate(self, data):
        """
        Validates the provided data for user registration. Checks for:
        1. Unique username
        2. Password match
        """
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Creates a new user with the given validated data. It removes the repeated_password from the validated data and uses the password to set the user's password. After saving the user, the user is returned.
        """
        validated_data.pop('repeated_password')
        password = validated_data.pop('password')  
        user = CustomUser(**validated_data)        
        user.set_password(password)                
        user.save()                                

        return user
    
    
    
  