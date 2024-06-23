from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    level = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.username


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
