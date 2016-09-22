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

            additional_validators = []
            if field.additional_validators:
                additional_validators = [field.additional_validators]

            self.fields[field.slug] = field_type(
                label=field.label,
                initial=field.initial,
                required=field.required,
                disabled=field.disabled,
                help_text=field.help_text,
                validators=additional_validators
            )

            # Adds the field choices and max_length but catches the exception
            # as not all fields allow for these attrs.
            try:
                self.fields[field.slug].choices = field.choices
            except TypeError:
                pass
            try:
                self.fields[field.slug].choices = field.max_length
            except TypeError:
                pass

            # Adds widget-specific options to the form field
            widget_attrs = self.fields[field.slug].widget.attrs
            widget_attrs["placeholder"] = field.placeholder
