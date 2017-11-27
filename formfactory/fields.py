import markdown

from django.forms.fields import Field
from django.utils.text import mark_safe
from django.utils.translation import ugettext as _

from formfactory import widgets


class ParagraphField(Field):
    widget = widgets.ParagraphWidget

    def __init__(self, paragraph="", *args, **kwargs):
        super(ParagraphField, self).__init__(*args, **kwargs)

        # Always empty out label for a paragraph field.
        self.label = ""

        # No matter what is set, this field should never be required.
        self.required = False
        self.widget.is_required = False

        # Fields should handle their own args not being set.
        if paragraph == "":
            paragraph = _("Please set a value for this field.")

        # Pass the paragraph text to the widget without needing to override
        # widget __init__. Process markdown here, its up to custom fields to
        # worry about what they are trying to do, not factory.py
        data = {
            "base_attrs": self.widget.attrs,
            "extra_attrs": {"paragraph": markdown.markdown(paragraph)}
        }
        attrs = self.widget.build_attrs(**data)
        self.widget.attrs = attrs
