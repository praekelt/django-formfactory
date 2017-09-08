from django.forms.fields import Field

from formfactory import widgets


# TODO add support for paragraph field. Mark safe in templates.
class ParagraphField(Field):
    widget = widgets.ParagraphWidget

