from django import forms
from django.db import models

from formfactory import _registery, SETTINGS


FIELD_TYPES = tuple(
    (field, field) for field in SETTINGS["field-types"]
    if issubclass(getattr(forms.fields, field), forms.fields.Field)
)

ADDITIONAL_VALIDATORS = tuple(
    (validator.__name__, validator.__name__)
    for validator in _registery.get("validators", [])
)

FORM_ACTIONS = tuple(
    (action.__name__, action.__name__)
    for action in _registery.get("actions", [])
)


class FormFactory(forms.Form):
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

            # Add the field choices but catch the exception as not all fields
            # allow for them.
            try:
                self.fields[field.slug].choices = field.choices
            except TypeError:
                pass


class Form(models.Model):
    """
    Form model which encompasses a set of form fields and defines an action
    when the form processed.
    """
    title = models.CharField(
        max_length=256, help_text="A short descriptive title."
    )
    slug = models.SlugField(
        max_length=256, db_index=True, unique=True
    )
    action = models.CharField(
        choices=FORM_ACTIONS, max_length=128
    )

    class Meta:
        ordering = ["title"]

    def __unicode__(self):
        return self.title

    def as_form(self):
        """
        Builds the form factory object and returns it.
        """
        return FormFactory(fields=self.fields.all())


class FieldChoice(models.Model):
    """
    Defines options for select or multiselect field types.
    """
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    class Meta:
        ordering = ["label"]

    def __unicode__(self):
        return "%s:%s" % (self.label, self.value)


class FormField(models.Model):
    """
    Defines a form field with all option and required attributes.
    """
    title = models.CharField(
        max_length=256,
        help_text="A short descriptive title."
    )
    slug = models.SlugField(
        max_length=256, db_index=True, unique=True
    )
    position = models.PositiveIntegerField(default=0)
    form = models.ForeignKey(Form, related_name="fields")
    field_type = models.CharField(choices=FIELD_TYPES, max_length=128)
    label = models.CharField(max_length=64)
    initial = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=64)
    required = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)
    choices = models.ManyToManyField(FieldChoice)
    additional_validators = models.CharField(
        choices=ADDITIONAL_VALIDATORS, max_length=128, blank=True, null=True
    )

    class Meta:
        ordering = ["position"]

    def __unicode__(self):
        return self.title
