from django.db import models

# Create your models here.
class Picture(models.Model):
    category = models.CharField(max_length=25)
    photo = models.ImageField()
    edited = models.BooleanField(default=False)
