from rest_framework import serializers
from .models import Order
from offers_app.models import Offer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'customer_user', 'business_user',  'title', 'price', 'features', 'revisions', 'delivery_time', 'offer_type', 'status', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.Serializer):        
    offer_detail_id = serializers.IntegerField()
    
    def validate_offer_detail_id(self, value):
        try:
            offer = Offer.objects.get(pk=value)
        except Offer.DoesNotExist:
            raise serializers.ValidationError("Offer not found.")
        return offer
    
    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        offer = validated_data['offer_detail_id']

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
            delivery_time=offer.delivery_time_in_days,
            offer_type=offer.offer_type,
            status='in_progress',
        )
        
        