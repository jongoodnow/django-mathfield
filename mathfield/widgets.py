from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import textwrap

class MathFieldWidget(forms.Textarea):
    
    def render(self, name, value, attrs=None):
        output = super(MathFieldWidget, self).render(name, value, attrs)

        output += textwrap.dedent("""
            <script type="text/javascript" src="/static/mathfield/katex/katex.min.js"></script>
            <script type="text/javascript" src="/static/mathfield/js/mathfield.js"></script>
            <script type="text/javascript">
                renderMathFieldForm('%s');
            </script>
        """ %attrs['id'])

        return mark_safe(output)