from rest_framework import serializers
from django.conf import settings
from user_auth_app.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            'user',
            'username', 'first_name', 'last_name', 'file',
            'location', 'tel', 'description', 'working_hours',
            'type', 'email', 'created_at'
        ]
        read_only_fields = ['user', 'username', 'type', 'created_at']

   
    def update(self, instance, validated_data):
        """Ensure only allowed fields can be updated."""
        return super().update(instance, validated_data)

class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at'
        ]
    
    def to_representation(self, instance):
        """
        If any of the following fields are None, set them to an empty string in the serialized output:

            first_name
            last_name
            tel
            location
            description
            working_hours

        Done to prevent a KeyError when rendering the profile page.
        """
        representation = super().to_representation(instance)
        for field in ['first_name', 'last_name', 'tel', 'location', 'description', 'working_hours']:
            if representation.get(field) is None:
                representation[field] = ''
        return representation


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'email', 'created_at', 'uploaded_at', 'type']









