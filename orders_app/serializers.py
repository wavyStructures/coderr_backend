from rest_framework import serializers
from .models import Order
from offers_app.models import Offer, OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'id', 'customer_user', 'business_user', 'title', 'price',
            'features', 'revisions', 'delivery_time_in_days', 'offer_type',
            'status', 'created_at', 'updated_at'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):        
    offer_detail_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'title', 'price',
            'features', 'revisions', 'delivery_time_in_days', 'offer_type',
            'status', 'created_at', 'updated_at', 'offer_detail_id'
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def validate_offer_detail_id(self, value):
        try:
            offer_detail = OfferDetail.objects.get(pk=value)
        except Offer.DoesNotExist:
            raise serializers.ValidationError("Offer not found.")
        return offer_detail
    
    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        offer_detail = validated_data.pop('offer_detail_id')
        offer = offer_detail.offer
        # offer = validated_data['offer_detail_id']

        if user.type != 'customer':
            raise serializers.ValidationError("Only customers can place orders.")
        
        return Order.objects.create(
            customer_user=user,
            business_user=offer.business_user,
            offer=offer,
            title=offer.title,
            price=offer.price,
            features=offer.features,
            revisions=offer.revisions,
            delivery_time_in_days=offer.delivery_time_in_days,
            offer_type=offer.offer_type,
            status='in_progress',
        )
        

        
        