from django.test import TestCase
from collections import namedtuple
import mathfield.api as api

class APITestCase(TestCase):

    def test_serialize(self):
        self.assertEqual(api.get_math(), {
            'raw': '', 'html': '',
        })
        self.assertEqual(api.get_math('foo', 'bar'), {
            'raw': 'foo', 'html': 'bar',
        })
        self.assertEqual(api.get_math('no math'), {
            'raw': 'no math', 'html': 'no math',
        })
