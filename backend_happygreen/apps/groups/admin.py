# apps/groups/admin.py
from django.contrib import admin
from .models import EcoGroup, EcoGroupMembership  # ← Aggiornato i nomi

@admin.register(EcoGroup)
class EcoGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'is_private', 'created_at']
    list_filter = ['is_private', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['invite_code']

@admin.register(EcoGroupMembership)
class EcoGroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['user__username', 'group__name']