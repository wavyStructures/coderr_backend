from rest_framework import serializers
from .models import CustomUser 


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
            "user_type",  
            "email",
            "created_at"
        ]
                
        read_only_fields = ["id", "username", "email", "is_active"]   

    def update(self, instance, validated_data):

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
            'user_type'
        ]

    def get_user(self, obj):
        return obj.user.id 

    
class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True, required=True) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'user_type']
        
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False}  
        }  

    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')

        password = validated_data.pop('password')  
        user = CustomUser(**validated_data)        
        user.set_password(password)                
        user.save()                                

        return user
    
    
    
  