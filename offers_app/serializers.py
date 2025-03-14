from rest_framework import serializers
from .models import Offer

class OfferSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'
        

