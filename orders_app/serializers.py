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
            'id', 'offer_detail_id', 'customer_user', 'business_user', 'title',
            'features', 'revisions', 'delivery_time_in_days',  'price','features', 'offer_type',
            'status', 'created_at', 'updated_at' 
        ]
        read_only_fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at'
        ]

    def validate_offer_detail_id(self, value):
        from django.db.models import QuerySet

        try:
            offer_detail = OfferDetail.objects.get(pk=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("Offer not found.")
        return value
 
    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if user.type != 'customer':
            raise serializers.ValidationError("Only customers can place orders.")
        
        offer_detail_id = validated_data.pop('offer_detail_id', None)
        if not offer_detail_id:
            raise serializers.ValidationError("Offer detail ID is missing.")
        
        
        try:
            offer_detail = OfferDetail.objects.select_related('offer', 'offer__user').get(pk=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("Offer detail not found.")
        
        return Order.objects.create(
            customer_user=user,
            business_user=offer_detail.offer.user,
            offer=offer_detail.offer,
            
            title=offer_detail.title,
            price=offer_detail.price,
            
            features=offer_detail.features,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            
            offer_type=offer_detail.offer_type,
            status='in_progress',
        )
    



        