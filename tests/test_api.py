from django.test import TestCase
import mathfield.api as api

class APITestCase(TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_store_math_blank(self):
        self.assertEqual(api.store_math(), {'raw': '', 'html': '',})

    def test_store_math_html_given(self):
        self.assertEqual(api.store_math('foo', 'bar'), 
            {'raw': 'foo', 'html': 'bar',})

    def test_store_math_no_math(self):
        self.assertEqual(api.store_math('no math'), 
            {'raw': 'no math', 'html': 'no math',})

    def test_store_math_latex_in_body(self):
        self.assertEqual(api.store_math('foo $x=2$'), {
            'raw': 'foo $x=2$', 
            'html': """foo <span class="katex"><span class="katex-inner"><span class="strut" style="height:0.64444em;"></span><span class="strut bottom" style="height:0.64444em;vertical-align:0em;"></span><span class="base textstyle uncramped"><span class="mord mathit">x</span><span class="mrel">=</span><span class="mord">2</span></span></span></span>"""
        })

    def test_store_math_latex_at_start(self):
        self.assertEqual(api.store_math('$x=2$'), {
            'raw': '$x=2$', 
            'html': """<span class="katex"><span class="katex-inner"><span class="strut" style="height:0.64444em;"></span><span class="strut bottom" style="height:0.64444em;vertical-align:0em;"></span><span class="base textstyle uncramped"><span class="mord mathit">x</span><span class="mrel">=</span><span class="mord">2</span></span></span></span>"""
        })

    def test_store_math_escaped_dollars(self):
        self.assertEqual(api.store_math('\\$foo$x=\\$ 2$bar\\$'), {
            'raw': '\\$foo$x=\\$ 2$bar\\$',
            'html': """$foo<span class="katex"><span class="katex-inner"><span class="strut" style="height:0.75em;"></span><span class="strut bottom" style="height:0.80556em;vertical-align:-0.05556em;"></span><span class="base textstyle uncramped"><span class="mord mathit">x</span><span class="mrel">=</span><span class="mord">$</span><span class="mord">2</span></span></span></span>bar$"""
        })
