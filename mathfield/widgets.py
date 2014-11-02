from django import forms
from django.forms import fields
from django.utils.safestring import mark_safe

class MathFieldForm(forms.ChoiceField, fields.CharField):
    pass

class MathFieldWidget(forms.TextInput):
    
    def render(self, name, value, attrs=None):
        output = super(MathFieldWidget, self).render(name, value, attrs)
        return mark_safe(output)