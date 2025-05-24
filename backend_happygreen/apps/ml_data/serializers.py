from rest_framework import serializers
from .models import ObjectCategory, ScannedObject, ProductBarcode, BarcodeSearch
from apps.authentication.serializers import UserProfileSerializer


class ObjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectCategory
        fields = '__all__'


class ScannedObjectSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    category = ObjectCategorySerializer(read_only=True)

    class Meta:
        model = ScannedObject
        fields = ['id', 'user', 'image', 'detected_object', 'confidence_score',
                  'category', 'latitude', 'longitude', 'eco_points_earned', 'created_at']
        read_only_fields = ['user', 'eco_points_earned', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user

        # Assegna punti eco per la scansione
        validated_data['eco_points_earned'] = 5

        scanned_object = ScannedObject.objects.create(**validated_data)

        # Aggiungi punti eco all'utente
        request.user.eco_points += scanned_object.eco_points_earned
        request.user.save()

        # Aggiorna il progresso delle sfide di scansione
        from apps.challenges.models import UserChallenge
        scan_challenges = UserChallenge.objects.filter(
            user=request.user,
            challenge__challenge_type='scan_objects',
            status='in_progress'
        )

        for user_challenge in scan_challenges:
            user_challenge.progress += 1
            if user_challenge.progress >= user_challenge.challenge.target_count:
                user_challenge.status = 'completed'
                user_challenge.completed_at = timezone.now()
                # Assegna punti bonus per completare la sfida
                request.user.eco_points += user_challenge.challenge.points_reward
                request.user.save()
            user_challenge.save()

        return scanned_object


class ProductBarcodeSerializer(serializers.ModelSerializer):
    category = ObjectCategorySerializer(read_only=True)

    class Meta:
        model = ProductBarcode
        fields = '__all__'


class BarcodeSearchSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    barcode = ProductBarcodeSerializer(read_only=True)

    class Meta:
        model = BarcodeSearch
        fields = ['id', 'user', 'barcode', 'searched_at']
        read_only_fields = ['user', 'searched_at']
