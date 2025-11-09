from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12,unique=True)
    img = models.ImageField(upload_to='profile', blank=True, null=True)
    reset_code=models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.phone}"

class Product(models.Model):
    COLOR_CHOICES = [
        ("red", "Red"),
        ("green", "Green"),
        ("blue", "Blue"),
        ("purple", "Purple"),
        ("brown", "Brown"),
        ("orange", "Orange"),
        ("yellow", "Yellow"),
        ("gray", "Gray"),
        ("pink", "Pink"),
        ("white", "White"),
    ]
    SIZE_CHOICES = [
        ("XS","XS"),
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL"),
        ("XXL","XXL"),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(choices=COLOR_CHOICES, max_length=20, blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=5, blank=True, null=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)