from django import forms
from django.utils.safestring import mark_safe
import textwrap
import json

class MathFieldWidget(forms.Textarea):
    
    def render(self, name, value, attrs=None):
        output = super(MathFieldWidget, self).render(name, value, attrs)
        output = '<div id="%s-container"><span>%s</span></div>' %(
            attrs['id'], output)
        valuedict = json.loads(value)
        raw = valuedict['raw'] if 'raw' in value else ''
        html = valuedict['html'] if 'html' in value else ''
        raw = raw.replace('\\', '\\\\')
        html = html.replace('"', '\\"')
        output += textwrap.dedent("""
            <script type="text/javascript" 
                src="/static/mathfield/katex/katex.min.js"></script>
            <script type="text/javascript" 
                src="/static/mathfield/js/mathfield.js"></script>
            <script type="text/javascript">
                renderMathFieldForm("%s", "%s", "%s");
            </script>
        """ %(attrs['id'], raw, html))

        return mark_safe(output)