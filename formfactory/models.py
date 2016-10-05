from django import forms
from django.db import models

from formfactory import actions, _registry, factory, SETTINGS, validators


actions.auto_discover()
validators.auto_discover()


FIELD_TYPES = tuple(
    (field, field) for field in SETTINGS["field-types"]
    if issubclass(getattr(forms.fields, field), forms.fields.Field)
)

ADDITIONAL_VALIDATORS = tuple(
    (validator, validator)
    for validator in validators.get_registered_validators()
)

FORM_ACTIONS = tuple(
    (action, action) for action in actions.get_registered_actions()
)


class FormData(models.Model):
    """A basic store for form data.
    """
    uuid = models.UUIDField(db_index=True)
    form = models.ForeignKey("Form")

    class Meta:
        ordering = ["uuid"]

    def __unicode__(self):
        return "%s (%s)" % (self.form.title, self.uuid)


class FormDataItem(models.Model):
    """A basic store for form data items.
    """
    form_data = models.ForeignKey(FormData, related_name="items")
    form_field = models.ForeignKey("FormField")
    value = models.TextField()


class Action(models.Model):
    """Defines a form action.
    """
    action = models.CharField(
        choices=FORM_ACTIONS, max_length=128
    )

    def __unicode__(self):
        return self.action

    @property
    def action_class(self):
        return _registry["actions"][self.action]


class ActionParam(models.Model):
    """Defines a constant that can be passed to the action function.
    """
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    action = models.ForeignKey(Action)

    def __unicode__(self):
        return "%s:%s" % (self.key, self.value)


class FormActionThrough(models.Model):
    """Through table for form actions which defines an order.
    """
    action = models.ForeignKey(Action)
    form = models.ForeignKey("Form")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Form Action"
        verbose_name_plural = "Form Actions"

    def __unicode__(self):
        return "%s (%s)" % (self.action.action, self.order)


class Form(models.Model):
    """Form model which encompasses a set of form fields and defines an action
    when the form processed.
    """
    title = models.CharField(
        max_length=256, help_text="A short descriptive title."
    )
    slug = models.SlugField(
        max_length=256, db_index=True, unique=True
    )
    actions = models.ManyToManyField(Action, through=FormActionThrough)
    success_message = models.CharField(max_length=256, blank=True, null=True)
    failure_message = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        ordering = ["title"]

    def __unicode__(self):
        return self.title

    @property
    def action_classes(self):
        return [
            action.action_class for action in self.actions.all()
        ]

    def as_form(self, data=None):
        """
        Builds the form factory object and returns it.
        """
        if not self.pk:
            raise AttributeError(
                "The model needs to be saved before a form can be generated."
            )

        return factory.FormFactory(
            data, fields=self.fields.all(), form_id=self.pk,
            actions=self.action_classes
        )


class FieldChoice(models.Model):
    """Defines options for select or multiselect field types.
    """
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    class Meta:
        ordering = ["label"]

    def __unicode__(self):
        return "%s:%s" % (self.label, self.value)


class FormField(models.Model):
    """Defines a form field with all options and required attributes.
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
    max_length = models.PositiveIntegerField(default=256)
    help_text = models.CharField(max_length=256, blank=True, null=True)
    label = models.CharField(max_length=64)
    placeholder = models.CharField(max_length=128, blank=True, null=True)
    required = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)
    choices = models.ManyToManyField(FieldChoice, blank=True, null=True)
    additional_validators = models.CharField(
        choices=ADDITIONAL_VALIDATORS, max_length=128, blank=True, null=True
    )

    class Meta:
        ordering = ["position"]

    def __unicode__(self):
        return self.title
