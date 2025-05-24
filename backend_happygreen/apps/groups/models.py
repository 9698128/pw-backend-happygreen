# apps/groups/models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class EcoGroup(models.Model):  # ← CAMBIATO DA Group A EcoGroup
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_eco_groups')
    members = models.ManyToManyField(
        User,
        through='EcoGroupMembership',
        related_name='joined_eco_groups'  # ← Aggiungi related_name
    )
    is_private = models.BooleanField(default=False)
    invite_code = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'eco_groups'


class EcoGroupMembership(models.Model):  # ← CAMBIATO DA GroupMembership A EcoGroupMembership
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(EcoGroup, on_delete=models.CASCADE)  # ← Aggiornato riferimento
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')
        db_table = 'eco_group_memberships'

    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.role})"