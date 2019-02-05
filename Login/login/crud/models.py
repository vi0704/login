from django.db import models
from django.contrib.auth.models import User


class Name(models.Model):
    name=models.CharField(max_length=100)
    Hobby=models.CharField(max_length=100)
    occupation=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class user_token(models.Model):
    token = models.CharField(default=None, blank=True, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)