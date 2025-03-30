from rest_framework import serializers
from .models import Offer, OfferDetail
from user_auth_app.serializers import CustomUserSerializer
from django.conf import settings

CustomUser = settings.AUTH_USER_MODEL 

class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializes individual offer details."""

    class Meta:
        model = OfferDetail
        fields = [
            "id", "title", "revisions", "delivery_time_in_days", 
            "price", "features", "offer_type"
        ]
    
        
class OfferSerializer(serializers.ModelSerializer):
    """Serializes Offer objects including related offer details."""
    
    user_details = CustomUserSerializer(source="user", read_only=True)  
    details = OfferDetailSerializer(many=True, read_only=True)  

    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description",
            "created_at", "updated_at", "details",
            "min_price", "min_delivery_time", "user_details"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user"]  # Prevent user modifications

    def create(self, validated_data):
        """Create an offer and its related details."""
        request = self.context.get("request")
        user = request.user if request else None
        
        # Ensure only business users can create offers
        if not user or user.type != "business":
            raise serializers.ValidationError({"error": "Only business users can create offers."})
        
        details_data = validated_data.pop("details", [])
        offer = Offer.objects.create(user=user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def update(self, instance, validated_data):
        """Allow partial updates to an offer."""
        # Only update the fields that are provided
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
