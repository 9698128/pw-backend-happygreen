from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture_url = models.CharField(max_length=500, blank=True, null=True, help_text="URL immagine profilo")
    eco_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Badge(models.Model):
    BADGE_TYPES = [
        ('eco_detective', 'Eco Detective'),
        ('recycling_hero', 'Recycling Hero'),
        ('green_explorer', 'Green Explorer'),
        ('sustainability_champion', 'Sustainability Champion'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    badge_type = models.CharField(max_length=50, choices=BADGE_TYPES)
    icon = models.ImageField(upload_to='badges/')
    points_required = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"