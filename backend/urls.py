from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

# Importe apenas o módulo de views do seu app fibonacci
from fibonacci import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rotas de API organizadas
    path('fibonacci/products/', include('fibonacci.urls.products_urls')), 
    path('fibonacci/users/', include('fibonacci.urls.user_urls')),
    path('fibonacci/orders/', include('fibonacci.urls.order_urls')),
    path('api/products/', include('fibonacci.urls.products_urls')),
    
    # Rota específica de encontros
    path('api/encontros/', views.getEncontros, name='encontros'),
]

# Configurações de mídia (remova as duplicatas)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)