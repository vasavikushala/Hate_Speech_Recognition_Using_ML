from django.db import models

class RegisterUserTable(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)