from django.contrib import admin
from .models import Product, Order, OrderItem, Review, ShippingAddress, Category, ProductImage, Exposicao, UserProfileAddress,ArtistProfile
from .models import Exposicao

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} 


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'countInstock', 'createAt']
    list_filter = ['category', 'brand', 'createAt']
    search_fields = ['name', 'brand']
    list_editable = ['price', 'countInstock']
    
    
    inlines = [ProductImageInline]
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   
    list_display = ['_id', 'user', 'createdAt', 'totalPrice', 'isPaid']
    list_filter = ['isPaid', 'createdAt']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'product', 'qty', 'price']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'createdAt']
    list_filter = ['rating']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['order', 'city', 'country']

@admin.register(Exposicao)
class EncontroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'artista', 'data_inicio', 'data_fim', 'local']
    list_filter = ['data_inicio', 'artista']
    search_fields = ['titulo', 'artista']


@admin.register(UserProfileAddress)
class UserProfileAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'state', 'postalCode', 'is_default']
    list_filter = ['user', 'state']
    search_fields = ['user__username', 'address', 'city']

@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'instagram']
    search_fields = ['user__username', 'location']
















