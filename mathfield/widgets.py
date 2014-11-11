from django import forms
from django.utils.safestring import mark_safe
from mathfield.api import get_math, NodeError
import textwrap
import json
import cgi

class MathFieldWidget(forms.Textarea):
    
    def render(self, name, value, attrs=None):
        output = super(MathFieldWidget, self).render(name, value, attrs)
        output = '<div id="%s-container"><span>%s</span></div>' %(
            attrs['id'], output)
        if value:
            raw = value['raw'] if 'raw' in value else ''
            html = value['html'] if 'html' in value else ''
            raw = cgi.escape(raw.replace('\\', '\\\\'))
            html = html.replace('"', '\\"')
        else:
            raw = html = ''
        output += textwrap.dedent("""
            <script type="text/javascript" 
                src="/static/mathfield/katex/katex.min.js"></script>
            <script type="text/javascript" 
                src="/static/mathfield/js/mathfield.js"></script>
            <script type="text/javascript"
                src="/static/mathfield/js/encoder.js"></script>
            <script type="text/javascript">
                renderMathFieldForm("%s", "%s", "%s");
            </script>
        """ %(attrs['id'], raw, html))

        return mark_safe(output)