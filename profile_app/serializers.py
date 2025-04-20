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

# Minimal user data – useful for public info, cards, etc.
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'first_name', 'last_name', 'file']



# Combines user data with extra profile fields using nesting
class CustomProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(source='*')  # neat trick: source='*' flattens CustomUser into this one

    class Meta:
        model = CustomUser
        fields = [
            'user', 'file', 'location', 'tel',
            'description', 'working_hours', 'type'
        ]



