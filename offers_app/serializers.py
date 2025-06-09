from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from .models import Offer, OfferDetail
from user_auth_app.serializers import CustomUserSerializer
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class OfferDetailSerializer(serializers.ModelSerializer):

    features = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
    price = serializers.FloatField()

    class Meta:
        model = OfferDetail

        fields = [
            "id", "title", "description", "revisions",
            "delivery_time_in_days", "price", "features", "offer_type"
        ]
        
    def get_url(self, obj):
        request = self.context.get("request")           
        if request is None:
            return None
        return reverse("offer-detail-retrieve", kwargs={"pk": obj.id}, request=request)


class PublicOfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id", "title", "image", "description", "details"
        ]

    def create(self, validated_data):
        details_data = validated_data.pop("details", [])
        request = self.context.get("request")
        user = request.user if request else None

        if not user or user.user_type != "business":
            raise serializers.ValidationError({"error": "Only business users can create offers."})

        offer = Offer.objects.create(user=user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

class OfferMiniDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]
        
    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

class OfferMiniDetailAbsoluteSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(
                reverse("offer-detail-retrieve", kwargs={"pk": obj.id}, request=request)
            )
        return reverse("offer-detail-retrieve", kwargs={"pk": obj.id})


class OfferUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username"]
        
        
class OfferSerializer(serializers.ModelSerializer):
    
    user_details = OfferUserDetailSerializer(source="user", read_only=True)
    details = OfferDetailSerializer(many=True, write_only=True, required=False)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description",
            "created_at", "updated_at", 
            "details",
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
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.method in ("POST", "PUT", "PATCH"):
            # write mode → accept incoming details
            fields["details"] = OfferDetailSerializer(many=True)
        else:
            view = request.parser_context.get("view") if request and request.parser_context else None
            action = getattr(view, 'action', None)

            use_full = False
            if isinstance(view, APIView):
                if view.__class__.__name__.lower().endswith("detailview"):
                    use_full = True
            else:
                use_full = (action == "retrieve")

            fields["details"] = OfferDetailSerializer(many=True, read_only=True) if use_full else OfferMiniDetailSerializer(many=True, read_only=True)

        return fields
        
    def create(self, validated_data):
        """Create an offer and its related details."""
        
        try:
            request = self.context.get("request")
            user = request.user if request else None
            
            print(user)
            print(user.user_type)
            
            if not user or user.user_type != "business":
                raise serializers.ValidationError({"error": "Only business users can create offers."})
            
            details_data = validated_data.pop("details", [])
            offer = Offer.objects.create(user=user, **validated_data)

            detail_objs = []
            for detail_data in details_data:
                detail = OfferDetail.objects.create(offer=offer, **detail_data)
                detail_objs.append(detail)

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
        details_data = validated_data.pop("details", None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if details_data is not None:
            instance.details.all().delete()

            detail_objs = []
            for detail_data in details_data:
                detail = OfferDetail.objects.create(offer=instance, **detail_data)
                detail_objs.append(detail)

            if detail_objs:
                instance.min_price = min(d.price for d in detail_objs)
                instance.min_delivery_time = min(d.delivery_time_in_days for d in detail_objs)
                instance.save()        

        return instance


class OfferRetrieveSerializer(OfferSerializer):
    details = OfferMiniDetailAbsoluteSerializer(many=True, read_only=True)

    class Meta(OfferSerializer.Meta):
        pass  # Use same fields, just override details serializer
    
    

