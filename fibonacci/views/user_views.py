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
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):  
    user = request.user 
    data = request.data
    
    user.first_name = data.get('name', user.first_name)
    user.username = data.get('email', user.username)
    user.email = data.get('email', user.email)
    
    if data.get('password') and data['password'] != "":
        user.password = make_password(data['password'])
    user.save()

    profile, created = ArtistProfile.objects.get_or_create(user=user)
    profile.location = data.get('location', profile.location)
    profile.bio = data.get('bio', profile.bio)
    
    if 'avatar' in request.FILES:
        profile.profile_image = request.FILES['avatar']
    if 'banner' in request.FILES:
        profile.banner_image = request.FILES['banner']
        
    profile.save()
    
    serializer = UserSerializerWithToken(user, many=False)
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
def getArtists(request):
    artists = User.objects.filter(artist_profile__is_artist=True)
    serializer = ArtistListSerializer(artists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
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