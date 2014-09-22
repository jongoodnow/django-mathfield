from django.db import models
from mathfield.models import MathField

class Math(models.Model):
    math =  MathField()