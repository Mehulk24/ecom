from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Product(models.Model):
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
    ]

    CATEGORY_CHOICES = [
        ('Ring', 'Ring'),
        ('Necklace', 'Necklace'),
        ('Earring', 'Earring'),
        ('Bracelet', 'Bracelet'),
    ]

    COLOR_CHOICES = [
        ('#FFD700', 'Gold'),
        ('#C0C0C0', 'Silver'),
        ('#B76E79', 'Rose Gold'),
        ('#D4AF37', 'Antique Gold'),
        ('#8A7967', 'Bronze'),
        ('#E5E4E2', 'Platinum'),
        ('#AA6C39', 'Copper'),
        ('#E0115F', 'Ruby Red'),
        ('#7CFC00', 'Emerald Green'),
        ('#1E90FF', 'Sapphire Blue'),
        ('#9932CC', 'Amethyst Purple'),
        ('#FF1493', 'Pink Diamond'),
        ('#FFFFFF', 'Pearl White'),
        ('#000000', 'Onyx Black'),
    ]

    name = models.CharField(max_length=255)
    gender_category = models.CharField(max_length=10, choices=GENDER_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES,default='')
    size = models.CharField(max_length=50, blank=True, null=True,default='')  # Example: "6", "M", "18cm"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_gallery/')

    def __str__(self):
        return f"{self.product.name} - Gallery Image"


    def __str__(self):
        return f"{self.name} - {self.category}"


class NewProduct(models.Model):
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
    ]

    CATEGORY_CHOICES = [
        ('Ring', 'Ring'),
        ('Necklace', 'Necklace'),
        ('Earring', 'Earring'),
        ('Bracelet', 'Bracelet'),
    ]

    COLOR_CHOICES = [
        ('#FFD700', 'Gold'),
        ('#C0C0C0', 'Silver'),
        ('#B76E79', 'Rose Gold'),
        ('#D4AF37', 'Antique Gold'),
        ('#8A7967', 'Bronze'),
        ('#E5E4E2', 'Platinum'),
        ('#AA6C39', 'Copper'),
        ('#E0115F', 'Ruby Red'),
        ('#7CFC00', 'Emerald Green'),
        ('#1E90FF', 'Sapphire Blue'),
        ('#9932CC', 'Amethyst Purple'),
        ('#FF1493', 'Pink Diamond'),
        ('#FFFFFF', 'Pearl White'),
        ('#000000', 'Onyx Black'),
    ]

    name = models.CharField(max_length=255)
    gender_category = models.CharField(max_length=10, choices=GENDER_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES,default='')
    size = models.CharField(max_length=50, blank=True, null=True,default='')  # Example: "6", "M", "18cm"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.name} - {self.category}"

class NewProductImage(models.Model):
    product = models.ForeignKey(NewProduct, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_gallery/')

    def __str__(self):
        return f"{self.product.name} - Gallery Image"


    def __str__(self):
        return f"{self.name} - {self.category}"
    
class BestProduct(models.Model):
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
    ]

    CATEGORY_CHOICES = [
        ('Ring', 'Ring'),
        ('Necklace', 'Necklace'),
        ('Earring', 'Earring'),
        ('Bracelet', 'Bracelet'),
    ]

    COLOR_CHOICES = [
        ('#FFD700', 'Gold'),
        ('#C0C0C0', 'Silver'),
        ('#B76E79', 'Rose Gold'),
        ('#D4AF37', 'Antique Gold'),
        ('#8A7967', 'Bronze'),
        ('#E5E4E2', 'Platinum'),
        ('#AA6C39', 'Copper'),
        ('#E0115F', 'Ruby Red'),
        ('#7CFC00', 'Emerald Green'),
        ('#1E90FF', 'Sapphire Blue'),
        ('#9932CC', 'Amethyst Purple'),
        ('#FF1493', 'Pink Diamond'),
        ('#FFFFFF', 'Pearl White'),
        ('#000000', 'Onyx Black'),
    ]

    name = models.CharField(max_length=255)
    gender_category = models.CharField(max_length=10, choices=GENDER_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES,default='')
    size = models.CharField(max_length=50, blank=True, null=True,default='')  # Example: "6", "M", "18cm"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.name} - {self.category}"
    
class BestProductImage(models.Model):
    product = models.ForeignKey(BestProduct, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_gallery/')

    def __str__(self):
        return f"{self.product.name} - Gallery Image"


    def __str__(self):
        return f"{self.name} - {self.category}"

    


    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Generic relation to either Product or NewProduct
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, default='Pending')
    order_number = models.CharField(max_length=20, default='', unique=True)
    order_date = models.DateTimeField(default=timezone.now)
    pyment_status = models.CharField(max_length=20, default='Pending')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    
    # Generic relation to Product, NewProduct, or BestProduct
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) in Order #{self.order.order_number}"


class HomeBanner(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title
    

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

