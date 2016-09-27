import uuid

from django import forms

from formfactory.models import FormData, FormDataItems


class FormFactory(forms.Form):
    """Builds a form class from defined fields passed to it by the Form model.
    """
    def __init__(self, *args, **kwargs):
        self.form_id = kwargs.pop("form_id")
        defined_fields = kwargs.pop("fields")

        super(FormFactory, self).__init__(*args, **kwargs)

        self.uuid = unicode(uuid.uuid4())

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
            self.fields[field.slug].pk = field.pk

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
        """Saves the data to the store specified on the model.
        """
        form_data = FormData.objects.create(
            uuid=self.uuid,
            form_id=self.form_id,
        )
        for key, value in self.cleaned_data.items():
            FormDataItems.objects.create(
                form_data=form_data,
                form_field_id=self.fields[key].pk,
                value=value
            )
        return form_data
