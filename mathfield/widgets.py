from django import forms
from django.utils.safestring import mark_safe

class MathFieldWidget(forms.Textarea):
    
    def render(self, name, value, attrs=None):
        output = super(MathFieldWidget, self).render(name, value, attrs)
        return output