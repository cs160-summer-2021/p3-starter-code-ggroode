from django.db import models

# Create your models here.
class Picture(models.Model):
    category = models.CharField(max_length=25)
    photo = models.ImageField()
    edited = models.BooleanField(default=False)

class Palette(models.Model):
    name = models.CharField(primary_key=True,max_length=25)
    colors = models.CharField(max_length=2000)
