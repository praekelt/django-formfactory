import uuid

from django import forms


class FormFactory(forms.Form):
    """Builds a form class from defined fields passed to it by the Form model.
    """
    uuid = forms.UUIDField(
        initial=unicode(uuid.uuid4()), widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        self.actions = kwargs.pop("actions")

        form_id = kwargs.pop("form_id")
        defined_fields = kwargs.pop("fields")

        super(FormFactory, self).__init__(*args, **kwargs)

        # Creates a hidden form id field
        self.fields["form_id"] = forms.CharField(
            initial=form_id, widget=forms.HiddenInput()
        )

        # Interates over the fields defined in the Form model and sets the
        # appropriate attributes.
        for field in defined_fields:
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

            # Saves the field model pk to the form field to prevent the need
            # for another query in the save method.
            self.fields[field.slug].field_pk = field.pk

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

    def save(self, *args, **kwargs):
        """Performs the required actions in the defined sequence.
        """
        for action in self.actions:
            action_instance = action()
            action_instance.run(form_instance=self)
