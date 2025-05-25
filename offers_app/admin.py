from django.contrib import admin
from .models import Offer, OfferDetail

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'min_price', 'min_delivery_time', 'created_at')

@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ('offer', 'offer_type', 'price', 'delivery_time_in_days')