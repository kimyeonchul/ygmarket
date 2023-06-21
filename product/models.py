from django.db import models
from django.conf import settings
# Create your models here.

class ProductSearch(models.Model):
    query = models.CharField(max_length=100, unique=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-count']

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50,unique=True,allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/category/{self.slug}'

class Product(models.Model):
    title = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/',blank=False)
    document = models.TextField(default='')
    address = models.CharField(max_length=30, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='products')

    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.SET_NULL)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_products', blank=True)
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}'

    def get_absolute_url(self):
        return f'/product/{self.pk}'

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

