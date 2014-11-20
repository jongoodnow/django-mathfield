from __future__ import unicode_literals
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
import textwrap
import json
import cgi

class MathFieldWidget(forms.Textarea):
    
    def render(self, name, value, attrs=None):
        output = super(MathFieldWidget, self).render(name, value, attrs)
        output = '<div id="{0}-container"><span>{1}</span></div>'.format(
            attrs['id'], output)

        if value:
            if isinstance(value, dict):
                raw = value['raw'] if 'raw' in value else ''
                html = value['html'] if 'html' in value else ''
                html = html.replace('"', '\\"').replace("'", "\\'")
            elif isinstance(value, basestring):
                raw = value
                html = ''
            raw = cgi.escape(raw.replace('\\', '\\\\'))
        else:
            raw = html = ''

        if hasattr(settings, 'STATIC_URL'):
            static_url = getattr(settings, 'STATIC_URL', {})
        else:
            static_url = '/static/'
        output += textwrap.dedent("""
            <link rel="stylesheet" type="text/css" 
                href="{static}mathfield/css/mathfield.css"/>
            <script type="text/javascript" 
                src="{static}mathfield/js/mathfield.min.js"></script>
            <script type="text/javascript">
                renderMathFieldForm("{id}", "{raw}", "{html}");
            </script>
        """.format(static=static_url, id=attrs['id'], raw=raw, html=html))

        return mark_safe(output)