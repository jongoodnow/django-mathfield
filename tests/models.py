from django.db import models
from django.contrib import admin
from mathfield.models import MathField

class Math(models.Model):
    math =  MathField()
    math2 = MathField()