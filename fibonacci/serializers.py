from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User  
from .models import Product, Order, OrderItem, Review, ShippingAddress, Category, ProductImage, Comment, ArtistProfile

class UserSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    bio = serializers.SerializerMethodField(read_only=True)
    location = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    banner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User  
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'bio', 'location', 'avatar', 'banner']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):  
        return obj.is_staff

    def get_name(self, obj):  
        name = obj.first_name
        if name == "":
            name = obj.email
        return name
    
    def get_bio(self, obj):
        try:
            return obj.artist_profile.bio or ""
        except:
            return ""
    
    def get_location(self, obj):
        try:
            return obj.artist_profile.location or ""
        except:
            return ""
    
    def get_avatar(self, obj):
        try:
            if obj.artist_profile.profile_image:
                return obj.artist_profile.profile_image.url
            return None
        except:
            return None
    
    def get_banner(self, obj):
        try:
            if obj.artist_profile.banner_image:
                return obj.artist_profile.banner_image.url
            return None
        except:
            return None


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = User 
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'bio', 'location', 'avatar', 'banner', 'token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return "Usuário Anônimo"


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = Product
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        return ReviewSerializer(reviews, many=True).data

    def get_comments(self, obj):
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True).data
    

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        return OrderItemSerializer(items, many=True).data

    def get_shippingAddress(self, obj):
        try:
            address = obj.shippingaddress 
            return ShippingAddressSerializer(address, many=False).data
        except:
            return None

    def get_user_details(self, obj):
        if obj.user:
            return UserSerializer(obj.user, many=False).data
        return None


class ArtistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistProfile
        fields = '__all__'


class ArtistListSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile']

    def get_profile(self, obj):
        try:
            profile = obj.artist_profile
            return ArtistProfileSerializer(profile, many=False).data
        except:
            return None