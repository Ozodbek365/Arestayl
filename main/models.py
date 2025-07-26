from itertools import count
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            base_slug = slug


            count = 0
            while Category.objects.filter(slug=slug).exists():
                base_slug = slug + str(count)
                count += 1

            self.slug = base_slug
        super().save(*args, **kwargs)

class SubCategory(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            base_slug = slug


            count = 0
            while SubCategory.objects.filter(slug=slug).exists():
                base_slug = slug + str(count)
                count += 1

            self.slug = base_slug
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    description = models.TextField(blank=True, null=True)
    guarantee = models.CharField(max_length=255, blank=True, null=True)
    delevery_time = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    views = models.PositiveIntegerField(default=0)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            base_slug = slug


            count = 0
            while Product.objects.filter(slug=slug).exists():
                base_slug = slug + str(count)
                count += 1

            self.slug = base_slug
        super().save(*args, **kwargs)

class Image(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.image

class Review(models.Model):
    comment = models.TextField(blank=True, null=True)
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    percentage = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    amount = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    end_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title