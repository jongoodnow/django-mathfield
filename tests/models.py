from django.db import models
from mathfield.models import MathField

class Lesson(models.Model):
    lesson_plan =  MathField(blank=True)