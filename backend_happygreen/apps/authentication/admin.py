from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Badge, UserBadge


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'eco_points', 'level', 'is_active']
    list_filter = ['is_active', 'is_staff', 'level', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = UserAdmin.fieldsets + (
        ('Eco Profile', {'fields': ('profile_picture', 'eco_points', 'level')}),
    )


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'points_required', 'created_at']
    list_filter = ['badge_type', 'created_at']
    search_fields = ['name', 'description']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']