django-mathfield
================

MathField is a model field that allows you to input LaTeX and store the compiled
HTML on your database. It comes with a form for the Django Admin that provides
live previews of your rendered LaTeX.

Installation and Setup
----------------------

Your server needs to have 
`Python 2.7 <https://www.python.org/downloads/release/python-278/>`_ and 
`Django 1.7 <https://www.djangoproject.com/download/>`_. Python 3 support is 
coming soon.

Get it installed with::

    $ pip install django-mathfield

Add :code:`'mathfield'` to your :code:`INSTALLED_APPS` in your Django project's
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

Developer API
-------------

You can modify MathFields and compile LaTeX on your server without the admin
form if you would like. To be able to compile LaTeX serverside, you must have
`node.js <http://nodejs.org/download/>`_ (v0.10+) installed and it must be on 
your system path as an executable called :code:`node`. Note that this is not
necessary if you just use the admin form, as all compilation will occur in the
browser in this case.

Instantiating Models
********************

There are two ways to pass data to a MathField: as a string, or as a dictionary
with the keys :code:`raw` and :code:`html`. If you pass a string, the html will
be rendered for you.

Let's say you are using the :code:`Lesson` model from above, which has a
:code:`lesson_plan` column that is a MathField. You can create a new instance
with::

.. code:: python
    
    new_lesson = Lesson(lesson_plan='One half is $\\frac{1}{2}$.')
    new_lesson.save()

You can also pass a dictionary that contains the raw text under the key
:code:`raw` and the already rendered HTML under the key :code:`html`. This is
particularly useful if you want to generate the HTML yourself, perhaps because
you can't install node.js on your server, or you want to use a typesetting
library other than `KaTeX <https://github.com/Khan/KaTeX>`_.

The function :code:`store_math` provided in the mathfield API is provided for
convenience. If you don't know the HTML, you don't have to provide it, and it
will be generated for you. Otherwise, you can pass in the HTML and it will just
use that. For example::

.. code:: python

    import mathfield

    # if you already know the HTML:
    math_data = mathfield.store_math(raw_text, html)

    # if you don't:
    math_data = mathfield.store_math(raw_text)

    new_lesson = Lesson(lesson_plan=math_data)
    new_lesson.save()

Database Lookups
****************

When you look up an existing MathField, you get a dictionary with the keys
:code:`raw` and :code:`html`::

.. code:: python

    lesson = Lesson.objects.get(id=0)
    print lesson.lesson_plan['raw']
    # One half is $\frac{1}{2}$

    print lesson.lesson_plan['html']
    # the html for your template...

Just Getting Some HTML
**********************

If you just want to pass in a string and get the HTML, use 
:code:`render_to_html`::

.. code:: python

    import mathfield
    
    html = mathfield.render_to_html('One half is $\\frac{1}{2}$.')