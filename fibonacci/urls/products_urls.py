from django.urls import path
from fibonacci.views import product_views as views 

urlpatterns = [
    # 1. Rotas fixas primeiro
    path('', views.getProducts, name="products"),
    path('create/', views.createProduct, name="product-create"),
    path('top/', views.getTopProducts, name="top-products"),
    path('categories/', views.getCategories, name="categories"), 
    path('featured/', views.getFeaturedProducts, name='featured-products'),
    path('category/<str:category_name>/', views.getProductsByCategory, name='products-by-category'),
    
    # 2. Rotas dinâmicas com <str:pk> por último
    path('<str:pk>/reviews/', views.createProductReview, name="create-review"),
    path('<str:pk>/', views.getProduct, name="product"),
]