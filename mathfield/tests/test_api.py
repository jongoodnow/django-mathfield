from django.test import TestCase
from collections import namedtuple
import mathfield.api as api

class APITestCase(TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_get_math(self):
        self.assertEqual(api.get_math(), {'raw': '', 'html': '',})
        self.assertEqual(api.get_math('foo', 'bar'), 
            {'raw': 'foo', 'html': 'bar',})
        self.assertEqual(api.get_math('no math'), 
            {'raw': 'no math', 'html': 'no math',})
        self.assertEqual(api.get_math('foo $x=2$'), {
            'raw': 'foo $x=2$', 
            'html': """foo <span class="katex"><span class="katex-inner"><span class="strut" style="height:0.64444em;"></span><span class="strut bottom" style="height:0.64444em;vertical-align:0em;"></span><span class="base textstyle uncramped"><span class="mord mathit">x</span><span class="mrel">=</span><span class="mord">2</span></span></span></span>"""
        })
        self.assertEqual(api.get_math('$x=2$'), {
            'raw': '$x=2$', 
            'html': """<span class="katex"><span class="katex-inner"><span class="strut" style="height:0.64444em;"></span><span class="strut bottom" style="height:0.64444em;vertical-align:0em;"></span><span class="base textstyle uncramped"><span class="mord mathit">x</span><span class="mrel">=</span><span class="mord">2</span></span></span></span>"""
        })
