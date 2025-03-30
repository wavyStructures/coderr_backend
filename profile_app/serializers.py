from rest_framework import serializers
from django.conf import settings

CustomUser = settings.AUTH_USER_MODEL

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "first_name", "last_name", "file",
            "location", "tel", "description", "working_hours",
            "type", "email", "created_at"
        ]
        read_only_fields = ["id", "username", "type", "created_at"]

    def update(self, instance, validated_data):
        """Ensure only allowed fields can be updated."""
        # Optional: Prevent `email` from being updated unless explicitly allowed
        validated_data.pop("email", None)  # Remove email updates for security reasons

        return super().update(instance, validated_data)

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "first_name", "last_name",
            "file", "location", "tel", "description",
            "working_hours", "type"
        ]

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "first_name", "last_name",
            "file", "uploaded_at", "type"
        ]
        
