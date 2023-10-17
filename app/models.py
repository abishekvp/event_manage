from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    
class Image(models.Model):
    image = models.ImageField(upload_to='images/')