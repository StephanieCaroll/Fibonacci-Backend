from django.urls import path
from ..views import artists_views as views

urlpatterns = [
    path('', views.getArtists, name='artists'),
    path('<str:pk>/', views.getArtistById, name='artist-details'),
]