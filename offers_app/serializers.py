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
    """Serializes Offer objects including nested OfferDetails."""
    annotated_min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    annotated_min_delivery_time = serializers.IntegerField(read_only=True)
    
    user_details = CustomUserSerializer(source="user", read_only=True)  
    details = OfferDetailSerializer(many=True)  


    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description",
            "created_at", "updated_at", "details",
            "annotated_min_price", 
            "annotated_min_delivery_time",
            "user_details"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user", "annotated_min_price", "annotated_min_delivery_time"]

    def get_details(self, obj):
        return [
            {"id": detail.id, "url": f"/api/offerdetails/{detail.id}/"}
            for detail in obj.details.all()
        ]
    
    
    def create(self, validated_data):
        """Create an offer and its related details."""
        request = self.context.get("request")
        user = request.user if request else None
        
        if not user or user.type != "business":
            raise serializers.ValidationError({"error": "Only business users can create offers."})
        
        details_data = validated_data.pop("details", [])
        offer = Offer.objects.create(user=user, **validated_data)

        detail_objs = []
        for detail_data in details_data:
            detail = OfferDetail.objects.create(offer=offer, **detail_data)
            detail_objs.append(detail)

        # Update min_price and min_delivery_time based on OfferDetails
        offer.min_price = min([d.price for d in detail_objs])
        offer.min_delivery_time = min([d.delivery_time_in_days for d in detail_objs])
        offer.save()
            
        return offer

    def update(self, instance, validated_data):
        """
        Allow partial updates to an offer.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
