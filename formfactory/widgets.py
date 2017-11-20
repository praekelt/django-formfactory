import django
from django.forms.utils import flatatt
from django.forms.widgets import Widget
from django.utils.html import format_html

# TODO Add django 19 and 110 render support
class ParagraphWidget(Widget):
    template_name = "formfactory/forms/widgets/paragraph.html"

    def render(self, *args, **kwargs):
        if django.VERSION[1] >= 11:
            return super(ParagraphWidget, self).render(*args, **kwargs)
        else:
            return format_html(self.attrs["paragraph"])
