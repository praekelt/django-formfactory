from django import forms


class FormFactory(forms.Form):
    """
    Builds a form class from defined fields passed to it by the Form model.
    """
    def __init__(self, *args, **kwargs):
        self.defined_fields = kwargs.pop("fields")
        super(FormFactory, self).__init__(*args, **kwargs)

        # Interates over the fields defined in the Form model and sets the
        # appropriate attributes.
        for field in self.defined_fields:
            field_type = getattr(forms, field.field_type)
            self.fields[field.slug] = field_type(
                label=field.label,
                initial=field.initial,
                required=field.required,
                disabled=field.disabled,
                validators=[field.additional_validators]
            )

            # Adds the field choices but catches the exception as not all
            # fields allow for them.
            try:
                self.fields[field.slug].choices = field.choices
            except TypeError:
                pass

            # Adds widget-specific options to the form field
            widget_attrs = self.fields[field.slug].widget.attrs
            widget_attrs["placeholder"] = field.placeholder
