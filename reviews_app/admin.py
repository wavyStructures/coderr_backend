from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'reviewer',
        'business_user',
        'rating',
        'short_description',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'rating',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'reviewer__username',
        'business_user__username',
        'description',
    )
    ordering = ('-created_at',)

    def short_description(self, obj):
        """
        If the description is longer than 50 characters, return the first 50
        characters with an ellipsis at the end. Otherwise, return the description
        as is.
        """
        return (obj.description[:50] + '...') if len(obj.description) > 50 else obj.description

    short_description.short_description = 'Description'
