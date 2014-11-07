from django.db import models
import json

class MathField(models.TextField):

    description = 'Field that allows you to write LaTeX and display it as HTML.'

    def to_python(self, value):
        """ The data gets stored into a single text field. The html appears 
            first and is contained with in a span with the class 'katex'. The 
            rest of the string is the raw input from the user.
        """
        if not value:
            return None
        return json.loads(value)

    def get_prep_value(self, value):
        return json.dumps(value)

    def formfield(self, **kwargs):
        defaults = {
            'help_text': 'Type text as you would normally. If you want to write LaTeX, surround it with $ characters.'
        }
        defaults.update(kwargs)
        field = super(MathField, self).formfield(**defaults)
        field.max_length = self.max_length
        return field