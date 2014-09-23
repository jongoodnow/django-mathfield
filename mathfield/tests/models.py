from django.db import models
from django.contrib import admin
from mathfield.models import MathField

class Math(models.Model):
    name = models.CharField(max_length=200)
    math =  MathField()

admin.site.register(Math)