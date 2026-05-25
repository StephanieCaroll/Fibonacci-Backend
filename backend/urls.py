from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static


from fibonacci import views

urlpatterns = [
    path('admin/', admin.site.urls),
    

    path('fibonacci/products/', include('fibonacci.urls.products_urls')), 
    path('fibonacci/users/', include('fibonacci.urls.user_urls')),
    path('fibonacci/orders/', include('fibonacci.urls.order_urls')),
    path('api/products/', include('fibonacci.urls.products_urls')),
    
    path('api/users/', include('fibonacci.urls.user_urls')),
    path('api/artists/', include('fibonacci.urls.artists_urls')),
   
   
    
    path('api/encontros/', views.getEncontros, name='encontros'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)