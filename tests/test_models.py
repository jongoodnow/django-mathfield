from django.test import TestCase
from tests.models import Math
from django.core import exceptions
import json

class ModelTestCase(TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty_field(self):
        Math.objects.create(id=0)
        obj = Math.objects.get(id=0)
        self.assertEqual(obj.math, {'raw': '', 'html': ''})

    def test_empty_dictionary_add(self):
        Math.objects.create(id=0, math={})
        obj = Math.objects.get(id=0)
        self.assertEqual(obj.math, {'raw': '', 'html': ''})

    def test_dictionary_add(self):
        Math.objects.create(id=0, math={'raw': '1', 'html': '2'})
        obj = Math.objects.get(id=0)
        self.assertEqual(obj.math, {'raw': '1', 'html': '2'})

    def test_bad_dictionary_add(self):
        try:
            Math.objects.create(math={'raw': '1', 'foo': '2'})
        except exceptions.ValidationError:
            pass # good!
        else:
            raise AssertionError

    def test_empty_string_add(self):
        Math.objects.create(id=0, math='')
        obj = Math.objects.get(id=0)
        self.assertEqual(obj.math, {'raw': '', 'html': ''})        

    def test_string_add(self):
        Math.objects.create(id=0, math=json.dumps({'raw': '1', 'html': '2'}))
        obj = Math.objects.get(id=0)
        self.assertEqual(obj.math, {'raw': '1', 'html': '2'})

    def test_raw_string_add(self):
        Math.objects.create(id=0, math="$x=2$")
        obj = Math.objects.get(id=0)
        self.assertEqual(obj.math, {
            'raw': '$x=2$', 
            'html': """<span class="katex"><span class="katex-inner"><span class="strut" style="height:0.64444em;"></span><span class="strut bottom" style="height:0.64444em;vertical-align:0em;"></span><span class="base textstyle uncramped"><span class="mord mathit">x</span><span class="mrel">=</span><span class="mord">2</span></span></span></span>"""
        })

    def test_bad_string_add(self):
        try:
            Math.objects.create(math=json.dumps({'raw': '1', 'foo': '2'}))
        except exceptions.ValidationError:
            pass # good!
        else:
            raise AssertionError
        