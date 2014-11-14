from django.contrib import admin
from django import forms
from mathfield.widgets import MathFieldWidget
from tests.models import Math

class MathAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'math': MathFieldWidget,
            'math2': MathFieldWidget
        }


class MathAdmin(admin.ModelAdmin):
    form = MathAdminForm


admin.site.register(Math, MathAdmin)