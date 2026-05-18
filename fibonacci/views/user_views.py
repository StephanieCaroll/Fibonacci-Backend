from django.shortcuts import render
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse 

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from fibonacci.models import *
from fibonacci.serializers import UserSerializer, UserSerializerWithToken, ArtistListSerializer, ProductSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v 
        return data 

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username  
        token['message'] = "Projeto Galeria de Artes"
        return token

class MyTokenObtainPairView(TokenObtainPairView):  
    serializer_class = MyTokenObtainPairSerializer 

@api_view(['POST'])  
@permission_classes([AllowAny]) 
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        
        profile, created = ArtistProfile.objects.get_or_create(user=user)
        profile.location = data.get('location', 'Brasil')
        profile.bio = data.get('bio', 'Nada a dizer')
        profile.is_artist = True
        profile.save()

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as e:  
        message = {"detail": "Utilizador com este e-mail já existe"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])  
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):  
    user = request.user 
    
    print("=" * 50)
    print("Dados recebidos no request.data:", dict(request.data))
    print("Arquivos recebidos:", request.FILES)
    print("=" * 50)
    
    if 'name' in request.data and request.data['name']:
        user.first_name = request.data['name']
    
    if 'email' in request.data and request.data['email']:
        user.email = request.data['email']
        user.username = request.data['email']
    
    user.save()

    profile, created = ArtistProfile.objects.get_or_create(user=user)
    profile.is_artist = True  # Garante que é artista
    
    if 'bio' in request.data:
        profile.bio = request.data['bio']
        print(f"Bio atualizada para: {profile.bio}")
    
    if 'location' in request.data:
        profile.location = request.data['location']
        print(f"Location atualizada para: {profile.location}")
    
    if 'avatar' in request.FILES:
        profile.profile_image = request.FILES['avatar']
        print(f"Avatar atualizado: {request.FILES['avatar'].name}")
    
    if 'banner' in request.FILES:
        profile.banner_image = request.FILES['banner']
        print(f"Banner atualizado: {request.FILES['banner'].name}")
    
    # Redes sociais
    if 'instagram' in request.data:
        profile.instagram = request.data['instagram']
    if 'facebook' in request.data:
        profile.facebook = request.data['facebook']
    if 'twitter' in request.data:
        profile.twitter = request.data['twitter']
        
    profile.save()
    
    serializer = UserSerializerWithToken(user, many=False)
    print("Dados retornados:", serializer.data)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, pk):
    try:
        userForDeletion = User.objects.get(id=pk)
        userForDeletion.delete()
        return Response({'detail': 'Usuário deletado com sucesso'})
    except User.DoesNotExist:
        return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])  
def getArtists(request):
    artists = User.objects.filter(artist_profile__is_artist=True)
    serializer = ArtistListSerializer(artists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny]) 
def getArtistProfileAndProducts(request, pk):
    try:
        artist = User.objects.get(id=pk)
        artist_serializer = ArtistListSerializer(artist, many=False)
        products = Product.objects.filter(user=artist)
        products_serializer = ProductSerializer(products, many=True)
        return Response({
            'artist': artist_serializer.data,
            'products': products_serializer.data
        })
    except User.DoesNotExist:
        return Response({'detail': 'Artista não encontrado'}, status=404)