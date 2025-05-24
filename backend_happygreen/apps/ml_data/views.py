from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import ObjectCategory, ScannedObject, ProductBarcode, BarcodeSearch
from .serializers import (
    ObjectCategorySerializer, ScannedObjectSerializer,
    ProductBarcodeSerializer, BarcodeSearchSerializer
)


class ObjectCategoryListView(generics.ListAPIView):
    queryset = ObjectCategory.objects.all()
    serializer_class = ObjectCategorySerializer
    permission_classes = [IsAuthenticated]


class ScannedObjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ScannedObjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ScannedObject.objects.filter(user=self.request.user).order_by('-created_at')


class UserScannedObjectsView(generics.ListAPIView):
    serializer_class = ScannedObjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ScannedObject.objects.filter(user=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_barcode(request):
    barcode = request.data.get('barcode')
    if not barcode:
        return Response({'error': 'Barcode is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = ProductBarcode.objects.get(barcode=barcode)

        # Salva la ricerca
        BarcodeSearch.objects.create(user=request.user, barcode=product)

        serializer = ProductBarcodeSerializer(product)
        return Response(serializer.data)

    except ProductBarcode.DoesNotExist:
        return Response({'error': 'Product not found in database'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_barcode_searches(request):
    searches = BarcodeSearch.objects.filter(user=request.user).order_by('-searched_at')[:20]
    serializer = BarcodeSearchSerializer(searches, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def classify_waste(request):
    """
    Endpoint per classificare i rifiuti - riceve un'immagine e restituisce
    il tipo di rifiuto e le istruzioni per lo smaltimento
    """
    if 'image' not in request.FILES:
        return Response({'error': 'Image is required'}, status=status.HTTP_400_BAD_REQUEST)

    image = request.FILES['image']

    # Qui normalmente integreresti un modello ML per il riconoscimento
    # Per ora simuliamo la classificazione
    waste_types = {
        'plastic': {
            'bin_type': 'Raccolta Plastica',
            'bin_color': 'Giallo',
            'instructions': 'Svuota e sciacqua il contenitore prima di gettarlo',
            'tips': 'Rimuovi tappi e etichette se possibile'
        },
        'glass': {
            'bin_type': 'Raccolta Vetro',
            'bin_color': 'Verde',
            'instructions': 'Rimuovi tappi metallici o di plastica',
            'tips': 'Non rompere il vetro, gettalo intero'
        },
        'paper': {
            'bin_type': 'Raccolta Carta',
            'bin_color': 'Blu',
            'instructions': 'Rimuovi nastri adesivi e graffette',
            'tips': 'La carta unta o sporca va nell\'indifferenziato'
        },
        'organic': {
            'bin_type': 'Raccolta Organico',
            'bin_color': 'Marrone',
            'instructions': 'Usa sacchetti biodegradabili',
            'tips': 'Non inserire liquidi o oli'
        }
    }

    # Simulazione: sceglie casualmente un tipo di rifiuto
    import random
    detected_type = random.choice(list(waste_types.keys()))
    waste_info = waste_types[detected_type]

    # Assegna punti eco per la classificazione
    request.user.eco_points += 3
    request.user.save()

    return Response({
        'detected_type': detected_type,
        'confidence': round(random.uniform(0.7, 0.95), 2),
        'bin_type': waste_info['bin_type'],
        'bin_color': waste_info['bin_color'],
        'instructions': waste_info['instructions'],
        'tips': waste_info['tips'],
        'eco_points_earned': 3
    })
