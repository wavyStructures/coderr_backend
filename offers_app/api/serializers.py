from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.reverse import reverse
from ..models import Offer, OfferDetail
from user_auth_app.api.serializers import CustomUserSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

CustomUser = get_user_model()

class OfferDetailSerializer(serializers.ModelSerializer):

    features = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
    price = serializers.FloatField()

    class Meta:
        model = OfferDetail

        fields = [
            "id", "title", "revisions",
            "delivery_time_in_days", "price", "features", "offer_type"
        ]
       
    def get_url(self, obj):
        """
        Returns the URL of the offer detail object if the request is available.
        """
    
        request = self.context.get("request")           
        if request is None:
            return None
        return reverse("offer-details-view", kwargs={"pk": obj.id}, request=request)
    
    def to_representation(self, instance):
        """
        Converts the price to an integer if it is a float with no decimal values.
        """
        data = super().to_representation(instance)
        price = data.get("price")

        if isinstance(price, float) and price.is_integer():
            data["price"] = int(price)

        return data


class PublicOfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id", "title", "image", "description", "details"
        ]

    def create(self, validated_data):
        """
        Creates a new offer with the given details.
        """
        details_data = validated_data.pop("details", [])
        request = self.context.get("request")
        user = request.user if request else None

        if not user or user.type != "business":
            raise serializers.ValidationError({"error": "Only business users can create offers."})

        offer = Offer.objects.create(user=user, **validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        """
        Update an existing offer instance with validated data.
        """

        request = self.context.get("request")
        if request and instance.user != request.user:
            raise PermissionDenied("Sie dürfen dieses Angebot nicht bearbeiten.")

        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")
                if not offer_type:
                    raise serializers.ValidationError(
                        {"offer_type": "Offer type is required."}
                    )

                try:
                    detail = instance.details.get(offer_type=offer_type)
                except OfferDetail.DoesNotExist:
                    raise serializers.ValidationError(
                        {"offer_type": "Offer type does not exist."}
                    )

                for key, value in detail_data.items():
                    if key != "offer_type":
                        setattr(detail, key, value)
                detail.save()
            
        all_details = instance.details.all()
        if all_details.exists():
            instance.min_price = min(d.price for d in all_details)
            instance.min_delivery_time = min(d.delivery_time_in_days for d in all_details)
            instance.save()

        return instance
    
    
class OfferMiniDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]
        
    def get_url(self, obj):
        request = self.context.get("request")
        return reverse("offer-details-view", kwargs={"pk": obj.id}, request=request)


class OfferSingleSerializer(serializers.ModelSerializer):
    min_price = serializers.FloatField(source='annotated_min_price')
    min_delivery_time = serializers.IntegerField(source='annotated_min_delivery_time')

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',  
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time'
        ]

    def get_fields(self):
        """
        Returns the fields of the serializer based on the request method.
        """
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.method in "GET":
            fields["details"] = OfferMiniDetailSerializer(many=True, read_only=True)
        else:
            fields["details"] = OfferDetailSerializer(many=True)
        return fields


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
        """
        Retrieve the minimum price for the offer.
        """
        return obj.min_price

    def get_min_delivery_time(self, obj):
        """
        Retrieve the minimum delivery time for the offer.
        """
        return obj.min_delivery_time    
    
    def get_fields(self):
        """
        Overwrite the get_fields method to dynamically set the fields for the 'details' attribute.

        Depending on the request method, the field is either set to `OfferDetailSerializer` or `OfferMiniDetailSerializer`.
        If the method is POST, PUT or PATCH, the `OfferDetailSerializer` is used, so the user can create or update offer details.
        If the method is GET, the `OfferMiniDetailSerializer` is used, so only the id, price and delivery time are retrieved.
        In all other cases, the `OfferDetailSerializer` is used, but with read_only=True, so the user can only retrieve the details, but not update or delete them.
        """    
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.method in ("POST", "PUT", "PATCH"):
            fields["details"] = OfferDetailSerializer(many=True)
        elif request and request.method == "GET":
            fields["details"] = OfferMiniDetailSerializer(many=True, read_only=True)
        else:
            fields["details"] = OfferDetailSerializer(many=True, read_only=True)
        return fields

    def create(self, validated_data):
        """
        Create an offer and its related details.
        """        
        try:
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

            if detail_objs:
                offer.min_price = min(d.price for d in detail_objs)
                offer.min_delivery_time = min(d.delivery_time_in_days for d in detail_objs)
                offer.save()
                
            return offer
        except Exception as e:
            raise serializers.ValidationError({"internal_error": str(e)})



