from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome da Categoria")
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name="Descrição da Categoria")
    _id = models.AutoField(primary_key=True, editable=False)
    image = models.ImageField(upload_to="categories/", null=True, blank=True, verbose_name="Imagem da Categoria")
    

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default="/images/placeholder.png", upload_to="images/")
    brand = models.CharField(max_length=200, null=True, blank=True, verbose_name="Artista / Artesão")
    is_featured = models.BooleanField(default=False, verbose_name="Destaque da Semana")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    countInstock = models.IntegerField(null=True, blank=True, default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self): 
        return f"{self.name or 'Sem nome'} | {self.brand or 'Sem marca'} | {self.price or 0.00}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAT = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDeliver = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.createdAt)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    ShippingPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Produto")
    image = models.ImageField(upload_to="products/gallery/", verbose_name="Foto Extra")
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foto Extra do Produto"
        verbose_name_plural = "Galeria de Fotos do Produto"

    def __str__(self):
        return f"Foto de {self.product.name}"
    
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return f"Comentário de {self.email if self.email else 'Anônimo'} no produto {self.product}"
    
class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile')
    is_artist = models.BooleanField(default=False)
    location = models.CharField(max_length=255, default='Recife, PE')
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='artists/', default='/sample_artist.png')
    banner_image = models.ImageField(null=True, blank=True, upload_to='banners/', default='/sample_banner.png')
    instagram = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Perfil de Artista - {self.user.username}"
class Exposicao(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    local = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='exposicoes/')

    class Meta:
        verbose_name = "Encontro"
        verbose_name_plural = "Nossos Encontros"

    def __str__(self):
        return self.titulo


class UserProfileAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_addresses')
    address = models.CharField(max_length=255, verbose_name="Rua/Logradouro")
    number = models.CharField(max_length=20, verbose_name="Número")
    complement = models.CharField(max_length=100, null=True, blank=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado (UF)")
    postalCode = models.CharField(max_length=20, verbose_name="CEP")
    is_default = models.BooleanField(default=False, verbose_name="Endereço Padrão")
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return f"{self.address}, {self.number} - {self.user.username}"