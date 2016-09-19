import inspect

from django.forms import fields
from django.db import models

from formfactory import _registery


FIELD_CLASSES = [
    getattr(fields, field) for field in dir(fields)
    if inspect.isclass(getattr(fields, field))
]

FIELD_TYPES = tuple(
    (field.__name__, field.__name__) for field in FIELD_CLASSES
    if issubclass(field, fields.Field)
)

ADDITIONAL_VALIDATORS = tuple(
    (validator.__name__, validator.__name__)
    for validator in _registery.get("validators", [])
)

FORM_ACTIONS = tuple(
    (action.__name__, action.__name__)
    for action in _registery.get("actions", [])
)


class Form(models.Model):
    title = models.CharField(
        max_length=256, help_text="A short descriptive title."
    )
    slug = models.SlugField(
        max_length=256, db_index=True,
    )
    action = models.CharField(
        choices=FORM_ACTIONS, max_length=128
    )

    class Meta:
        ordering = ["title"]

    def __unicode__(self):
        return self.title


class FieldChoice(models.Model):
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    class Meta:
        ordering = ["label"]

    def __unicode__(self):
        return "%s:%s" % (self.label, self.value)


class FormField(models.Model):
    title = models.CharField(
        max_length=256,
        help_text="A short descriptive title."
    )
    position = models.PositiveIntegerField()

    form = models.ForeignKey(Form)

    field_type = models.CharField(choices=FIELD_TYPES, max_length=128)
    label = models.CharField(max_length=64)
    initial = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=64)
    required = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)
    choices = models.ManyToManyField(FieldChoice)
    additional_validators = models.CharField(
        choices=ADDITIONAL_VALIDATORS, max_length=128
    )

    class Meta:
        ordering = ["position"]

    def __unicode__(self):
        return self.title
