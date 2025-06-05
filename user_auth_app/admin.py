from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'id',
        'username',
        'email',
        'user_type',
        'location',
        'tel',
        'is_guest',
        'is_staff',
        'is_superuser',
        'created_at',
    )
    list_filter = (
        'user_type',
        'is_guest',
        'is_staff',
        'is_superuser',
        'created_at',
    )
    search_fields = (
        'username',
        'email',
        'location',
        'tel',
    )
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('tel', 'location', 'file', 'uploaded_at', 'description')}),
        ('User Type & Status', {'fields': ('user_type', 'is_guest', 'working_hours')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'tel', 'location', 'is_guest', 'file'),
        }),
    )
