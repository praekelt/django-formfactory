import django
from django.forms.widgets import Widget
from django.utils.html import format_html

class ParagraphWidget(Widget):
    template_name = "formfactory/forms/widgets/paragraph.html"

    def render(self, *args, **kwargs):

        # Add a basic check for Django 2. No tests yet, just ensures it will
        # fire for it too.
        if django.VERSION[0] == 2 and django.VERSION[1] >= 1:
            return super().render(*args, **kwargs)
        else:
            return format_html(self.attrs["paragraph"])
