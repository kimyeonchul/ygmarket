from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import Product

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', default='images/person.png', null=True)
    recently_viewed_products = models.ManyToManyField(Product, related_name='viewed_users', blank=True)
    user_liked_products = models.ManyToManyField(Product, related_name='liked_users', blank=True)

    def get_user_products(self):
        return self.products.all()