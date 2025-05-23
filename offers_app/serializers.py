from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from .models import Offer, OfferDetail
from user_auth_app.serializers import CustomUserSerializer
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializes individual offer details."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        exclude = ["offer"]
        

    def get_url(self, obj):
        request = self.context.get("request")           
        if request is None:
            return None
        return reverse("offer-detail-retrieve", kwargs={"pk": obj.id}, request=request)

class OfferMiniDetailSerializer(serializers.ModelSerializer):
    """Serializes individual offer details."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]
    
    def get_url(self, obj):
        request = self.context.get("request")           
        if request is None:
            return None
        return reverse("offer-detail-main", kwargs={"pk": obj.id}, request=request)


class OfferUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username"]
        
class OfferSerializer(serializers.ModelSerializer):
    """Serializes Offer objects and dynamically chooses nested OfferDetails."""
    
    # details = OfferMiniDetailSerializer(many=True, read_only=True)

    user_details = OfferUserDetailSerializer(source="user", read_only=True)
    details_input = OfferDetailSerializer(many=True, write_only=True, required=False)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description",
            "created_at", "updated_at", 
            "details",
            "details_input",
            "min_price", 
            "min_delivery_time",
            "user_details"
        ]
        read_only_fields = ["id", "user", "user_details", "created_at", "updated_at"]

    def get_min_price(self, obj):
        return obj.min_price

    def get_min_delivery_time(self, obj):
        return obj.min_delivery_time    
    
    def get_fields(self):
        """Dynamically swap the `details` serializer based on context (view type)."""
        fields = super().get_fields()
        request = self.context.get("request")
        
        # Try to detect if this is a list view or detail view
        if request and request.parser_context:
            view = request.parser_context.get("view")
            action = getattr(view, 'action', None)  # if using ViewSet
            if isinstance(view, APIView):
                # Fallback: check view class
                if view.__class__.__name__.lower().endswith("detailview"):
                    use_full = True
                else:
                    use_full = False
            else:
                use_full = (action == "retrieve")

            if use_full:
                fields["details"] = OfferDetailSerializer(many=True, read_only=True)
            else:
                fields["details"] = OfferMiniDetailSerializer(many=True, read_only=True)
        else:
            # Default to minimal if uncertain
            fields["details"] = OfferMiniDetailSerializer(many=True, read_only=True)

        return fields
    
    def create(self, validated_data):
        """Create an offer and its related details."""
        
        try:
            request = self.context.get("request")
            user = request.user if request else None
            
            if not user or user.type != "business":
                raise serializers.ValidationError({"error": "Only business users can create offers."})
            
            details_data = validated_data.pop("details_input", [])
            offer = Offer.objects.create(user=user, **validated_data)

            detail_objs = []
            for detail_data in details_data:
                detail = OfferDetail.objects.create(offer=offer, **detail_data)
                detail_objs.append(detail)

            # Update min_price and min_delivery_time based on OfferDetails       
            if detail_objs:
                offer.min_price = min(d.price for d in detail_objs)
                offer.min_delivery_time = min(d.delivery_time_in_days for d in detail_objs)
                offer.save()
                
            return offer
        except Exception as e:
            raise serializers.ValidationError({"internal_error": str(e)})

    def update(self, instance, validated_data):
        """
        Allow partial updates to an offer and its related details.
        """
        details_data = validated_data.pop("details_input", None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if details_data is not None:
            # Optional: Clear existing details
            instance.details.all().delete()

            detail_objs = []
            for detail_data in details_data:
                detail = OfferDetail.objects.create(offer=instance, **detail_data)
                detail_objs.append(detail)

            # Update min_price and min_delivery_time again
            if detail_objs:
                instance.min_price = min(d.price for d in detail_objs)
                instance.min_delivery_time = min(d.delivery_time_in_days for d in detail_objs)
                instance.save()        

        return instance

