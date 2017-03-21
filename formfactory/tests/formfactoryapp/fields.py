"""
Test file: Used for testing importing of custom
field types
"""

from django.forms.fields import CharField


# Test subclass
class MyCustomCharField(CharField):
    pass

