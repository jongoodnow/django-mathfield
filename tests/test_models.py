from __future__ import unicode_literals
from django.test import TestCase
from tests.models import Lesson
from django.core import exceptions
import json

class ModelTestCase(TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty_field(self):
        Lesson.objects.create(id=0)
        obj = Lesson.objects.get(id=0)
        self.assertEqual(obj.lesson_plan, {'raw': '', 'html': ''})

    def test_empty_dictionary_add(self):
        Lesson.objects.create(id=0, lesson_plan={})
        obj = Lesson.objects.get(id=0)
        self.assertEqual(obj.lesson_plan, {'raw': '', 'html': ''})

    def test_dictionary_add(self):
        Lesson.objects.create(id=0, lesson_plan={'raw': '1', 'html': '2'})
        obj = Lesson.objects.get(id=0)
        self.assertEqual(obj.lesson_plan, {'raw': '1', 'html': '2'})

    def test_bad_dictionary_add(self):
        try:
            Lesson.objects.create(lesson_plan={'raw': '1', 'foo': '2'})
        except exceptions.ValidationError:
            pass # good!
        else:
            raise AssertionError

    def test_empty_string_add(self):
        Lesson.objects.create(id=0, lesson_plan='')
        obj = Lesson.objects.get(id=0)
        self.assertEqual(obj.lesson_plan, {'raw': '', 'html': ''})        

    def test_string_add(self):
        Lesson.objects.create(id=0, lesson_plan=json.dumps({'raw': '1', 'html': '2'}))
        obj = Lesson.objects.get(id=0)
        self.assertEqual(obj.lesson_plan, {'raw': '1', 'html': '2'})

    def test_raw_string_add(self):
        Lesson.objects.create(id=0, lesson_plan="$x=2$")
        obj = Lesson.objects.get(id=0)
        self.assertEqual(obj.lesson_plan, {
            'raw': '$x=2$', 
            'html': """<span class="katex"><span class="katex-inner"><span class="strut" style="height:0.64444em;"></span><span class="strut bottom" style="height:0.64444em;vertical-align:0em;"></span><span class="base textstyle uncramped"><span class="mord mathit">x</span><span class="mrel">=</span><span class="mord">2</span></span></span></span>"""
        })

    def test_bad_string_add(self):
        try:
            Lesson.objects.create(lesson_plan=json.dumps({'raw': '1', 'foo': '2'}))
        except exceptions.ValidationError:
            pass # good!
        else:
            raise AssertionError
        