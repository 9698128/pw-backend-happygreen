from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Badge, UserBadge
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    BadgeSerializer,
    UserBadgeSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_badges(request):
    user_badges = UserBadge.objects.filter(user=request.user).order_by('-earned_at')
    serializer = UserBadgeSerializer(user_badges, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def available_badges(request):
    badges = Badge.objects.all()
    serializer = BadgeSerializer(badges, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def award_points(request):
    """Assegna punti eco a un utente"""
    points = request.data.get('points', 0)
    if points > 0:
        request.user.eco_points += points
        # Calcola il livello basato sui punti
        request.user.level = (request.user.eco_points // 100) + 1
        request.user.save()

        # Controlla se l'utente ha guadagnato nuovi badge
        check_and_award_badges(request.user)

        return Response({
            'message': f'{points} eco points awarded!',
            'total_points': request.user.eco_points,
            'level': request.user.level
        })
    return Response({'error': 'Invalid points value'}, status=status.HTTP_400_BAD_REQUEST)


def check_and_award_badges(user):
    """Controlla e assegna badge automaticamente"""
    # Badge per punti eco
    if user.eco_points >= 100 and not user.badges.filter(badge__badge_type='eco_detective').exists():
        eco_detective_badge = Badge.objects.get(badge_type='eco_detective')
        UserBadge.objects.create(user=user, badge=eco_detective_badge)

    # Badge per oggetti scansionati
    scanned_count = user.scanned_objects.count()
    if scanned_count >= 10 and not user.badges.filter(badge__badge_type='recycling_hero').exists():
        recycling_badge = Badge.objects.get(badge_type='recycling_hero')
        UserBadge.objects.create(user=user, badge=recycling_badge)
