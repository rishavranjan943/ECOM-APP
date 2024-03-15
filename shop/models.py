from django.db import models
from datetime import date
from django.conf import settings
from users.models import *
# Create your models here.

class Product(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=120)
    price=models.FloatField()
    discount_price=models.FloatField()
    category=models.CharField(max_length=120)
    description=models.TextField()
    image=models.TextField()
    date=models.DateField(default=date.today)

    def __str__(self):
        return self.title
    
class Wishlist(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product=models.ManyToManyField(Product)

    def __str__(self):
        return self.user.email


class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product=models.ManyToManyField(Product)

    def __str__(self):
        return self.user.email
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)

    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address=models.TextField()
    city=models.CharField(max_length=120)
    state=models.CharField(max_length=120)
    zipcode=models.CharField(max_length=120)

    def __str__(self):
        return self.user.email