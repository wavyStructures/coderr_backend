from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'customer_user',
        'business_user',
        'offer',
        'price',
        'offer_type',
        'status',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'status',
        'created_at',
        'updated_at',
        'offer_type',
    )
    search_fields = (
        'title',
        'customer_user__username',
        'business_user__username',
        'offer__title',
    )
    ordering = ('-created_at',)
