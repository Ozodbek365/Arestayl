from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class GENDER(models.TextChoices):
        MALE = 'male', 'male'
        FEMALE = 'female', 'female'
    phone = models.CharField(max_length=13)
    gender = models.CharField(max_length=10, choices=GENDER.choices, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_full_address(self):
        return f"{self.country}, {self.city}"