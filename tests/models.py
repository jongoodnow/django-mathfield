from django.db import models
from django.contrib import admin
from mathfield.models import MathField

class Lesson(models.Model):
    lesson_plan =  MathField(blank=True)