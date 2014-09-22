from collections import namedtuple
from django.db import models
from bs4 import BeautifulSoup

class MathField(models.TextField):

    description = "A field that allows you to write LaTeX and display it as HTML."

    def to_python(self, value):
        """ The data gets stored into a single text field. The html appears first
            and is contained with in a span with the class 'katex'. The rest of
            the string is the raw input from the user."
        """
        if isinstance(value, LatexData):
            return value

        html_soup = BeautifulSoup(value)
        html = html_soup.find_all(class='katex')[0] # only the first instance
        raw = value[len(html):] # the rest of the string is the raw input

        return namedtuple(raw=raw, html=html)

    def get_prep_value(self, value):
        return ''.join(value.html, value.raw)