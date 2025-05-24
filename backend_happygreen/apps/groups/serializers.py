# apps/groups/serializers.py
from rest_framework import serializers
from .models import EcoGroup, EcoGroupMembership  # ← AGGIORNATO: EcoGroup e EcoGroupMembership
from django.contrib.auth import get_user_model

User = get_user_model()


class EcoGroupMembershipSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = EcoGroupMembership
        fields = ['user', 'user_username', 'role', 'joined_at']


class EcoGroupSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    members_count = serializers.SerializerMethodField()
    members_details = EcoGroupMembershipSerializer(source='ecogroupmembership_set', many=True, read_only=True)

    class Meta:
        model = EcoGroup
        fields = [
            'id', 'name', 'description', 'created_by', 'created_by_username',
            'is_private', 'invite_code', 'created_at', 'members_count', 'members_details'
        ]
        read_only_fields = ['created_by', 'invite_code', 'created_at']

    def get_members_count(self, obj):
        return obj.members.count()

    def create(self, validated_data):
        group = super().create(validated_data)
        # Aggiungi il creatore come admin del gruppo
        EcoGroupMembership.objects.create(
            user=group.created_by,
            group=group,
            role='admin'
        )
        return group