from django.forms.fields import Field

from formfactory import widgets


# TODO add support for paragraph field. Mark safe in templates.
class ParagraphField(Field):
    widget = widgets.ParagraphWidget
    def __init__(self, paragraph, *args, **kwargs):
        super(ParagraphField, self).__init__(*args, **kwargs)

        # Always empty out label for a pragraph field.
        self.label = ""

        # No matter what is set, this field should never be required.
        self.required = False
        self.widget.is_required = False

        # Pass the paragraph text to the widget without needing to override
        # widgit __init__.
        attrs = self.widget.build_attrs(self.widget.attrs,
            {"paragraph": paragraph}
        )
        self.widget.attrs = attrs
