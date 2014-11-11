django-mathfield
================

MathField is a model field that allows you to input LaTeX and store the compiled
HTML on your database. It comes with a form for the Django Admin that provides
live previews of your text.

Installation and Setup
----------------------

Your server needs to have Python 2.7 and Django 1.7. Python 3 support is coming
soon.

Get it installed with::

    $ pip install django-mathfield

Add :code:`'mathfield'` to your :code:`INSTALLED_APPS` in your Django Project's
:code:`settings.py`.

Add a :code:`MathField` to one of your models like this::

.. code:: python

    from django.db import models
    from mathfield.models import MathField

    class Lesson(models.Model):
        lesson_plan = MathField()

Get live previews of the rendered LaTeX while you're editing in the Django admin
by adding :code:`MathFieldWidget` as a widget when registering your model in
:code:`admin.py`::

.. code:: python

    from django.contrib import admin
    from django import forms
    from mathfield.widgets import MathFieldWidget
    from yourapp.models import Lesson

    class LessonAdminForm(forms.ModelForm):

        class Meta:
            widgets = {
                'lesson_plan': MathFieldWidget
            }


    class LessonAdmin(admin.ModelAdmin):
        form = LessonAdminForm


    admin.site.register(Lesson, LessonAdmin)

After adding some data to your database, you can output the rendered HTML to
a template::

    <!DOCTYPE HTML>
    <html>
        <head>
            {% load staticfiles %}
            <link rel="stylesheet" type="text/css" href="{% static 'mathfield/css/mathfield.css' %}">
        </head>
        <body>
            <div>
                Raw LaTeX: {{ lesson.lesson_plan.raw }}
            </div>
            <div>
                Rendered HTML: {{ lesson.lesson_plan.html|safe }}
            </div>
        </body>
    </html>

Make sure that you include the :code:`mathfield.css` stylesheet in your template
head, and include :code:`|safe` with with the MathField HTML value. This will
give Django permission to render the text in that field as HTML. It is safe to
do this provided that you only update the HTML using the form in the Django
admin or the functions provided in the MathField API. Be very careful when
updating the HTML yourself!