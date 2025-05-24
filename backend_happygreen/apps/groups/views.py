# apps/groups/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import EcoGroup, EcoGroupMembership  # ← AGGIORNATO: EcoGroup e EcoGroupMembership
from .serializers import EcoGroupSerializer, EcoGroupMembershipSerializer


class EcoGroupListCreateView(generics.ListCreateAPIView):
    serializer_class = EcoGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EcoGroup.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EcoGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EcoGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EcoGroup.objects.filter(members=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_group(request, invite_code):
    try:
        group = EcoGroup.objects.get(invite_code=invite_code)
        membership, created = EcoGroupMembership.objects.get_or_create(
            user=request.user,
            group=group,
            defaults={'role': 'member'}
        )

        if created:
            return Response({'message': 'Joined group successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already a member'}, status=status.HTTP_200_OK)

    except EcoGroup.DoesNotExist:
        return Response({'error': 'Invalid invite code'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_group(request, group_id):
    try:
        group = EcoGroup.objects.get(id=group_id)
        membership = EcoGroupMembership.objects.get(user=request.user, group=group)

        if membership.role == 'admin' and EcoGroupMembership.objects.filter(group=group, role='admin').count() == 1:
            return Response({'error': 'Cannot leave group as the only admin'}, status=status.HTTP_400_BAD_REQUEST)

        membership.delete()
        return Response({'message': 'Left group successfully'}, status=status.HTTP_200_OK)

    except (EcoGroup.DoesNotExist, EcoGroupMembership.DoesNotExist):
        return Response({'error': 'Group or membership not found'}, status=status.HTTP_404_NOT_FOUND)