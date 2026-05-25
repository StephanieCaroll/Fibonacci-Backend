from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import ArtistProfile
from ..serializers import ArtistProfileSerializer

@api_view(['GET'])
def getArtists(request):
    # Filtra apenas quem é artista no seu modelo
    profiles = ArtistProfile.objects.filter(is_artist=True) 
    serializer = ArtistProfileSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getArtistById(request, pk):
    try:
        profile = ArtistProfile.objects.get(id=pk)
        serializer = ArtistProfileSerializer(profile, many=False)
        return Response(serializer.data)
    except ArtistProfile.DoesNotExist:
        return Response({'detail': 'Artista não encontrado'}, status=404)