from django.db import models
import json

class MathField(models.TextField):

    description = "A field that allows you to write LaTeX and display it as HTML."

    def to_python(self, value):
        """ The data gets stored into a single text field. The html appears first
            and is contained with in a span with the class 'katex'. The rest of
            the string is the raw input from the user."
        """
        if isinstance(value, LatexData):
            return value

        json_dec = json.decoded.JSONDecoder()
        return json_dec.decode(value)

    def get_prep_value(self, value):
        return json.dumps(value)