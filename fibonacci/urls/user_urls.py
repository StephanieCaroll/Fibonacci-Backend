from django.urls import path
from fibonacci.views import user_views

urlpatterns = [
    path('login/', user_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', user_views.registerUser, name='register'),
    path('profile/', user_views.getUserProfile, name='user-profile'),
    path('profile/addresses/', user_views.getUserAddresses, name='user-addresses'),
    path('profile/addresses/add/', user_views.addAddress, name='add-address'),
    path('profile/addresses/delete/<str:pk>/', user_views.deleteAddress, name='delete-address'),
    path('profile/update/', user_views.updateUserProfile, name='user-profile-update'),
    path('delete/<str:pk>/', user_views.deleteUser, name='user-delete'),
    path('artists/', user_views.getArtists, name='artists'),
    path('artists/<str:pk>/', user_views.getArtistProfileAndProducts, name='artist-detail'),
    
    
]