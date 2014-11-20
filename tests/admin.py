from django.contrib import admin
from django import forms
from mathfield.widgets import MathFieldWidget
from tests.models import Lesson

class LessonAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'lesson_plan': MathFieldWidget,
        }


class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm


admin.site.register(Lesson, LessonAdmin)