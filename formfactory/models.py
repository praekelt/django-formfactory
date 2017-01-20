from django import forms
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from formfactory import actions, _registry, factory, SETTINGS, validators


actions.auto_discover()
validators.auto_discover()


FIELD_TYPES = tuple(
    (field, field) for field in SETTINGS["field-types"]
    if issubclass(getattr(forms.fields, field), forms.fields.Field)
)

WIDGET_TYPES = tuple(
    (widget, widget) for widget in SETTINGS["widget-types"]
    if issubclass(getattr(forms.widgets, widget), forms.widgets.Widget)
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

    class Meta(object):
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
    action = models.CharField(choices=FORM_ACTIONS, max_length=128)

    def __unicode__(self):
        return self.action

    @property
    def as_function(self):
        return _registry["actions"][self.action]


class ActionParam(models.Model):
    """Defines a constant that can be passed to the action function.
    """
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    action = models.ForeignKey(Action, related_name="params")

    def __unicode__(self):
        return "%s:%s" % (self.key, self.value)


class FormActionThrough(models.Model):
    """Through table for form actions which defines an order.
    """
    action = models.ForeignKey(Action)
    form = models.ForeignKey("Form")
    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]
        verbose_name = "Form Action"
        verbose_name_plural = "Form Actions"

    def __unicode__(self):
        return "%s (%s)" % (self.action.action, self.order)


class BaseFormModel(models.Model):
    """Form model which encompasses a set of form fields and defines an action
    when the form processed.
    """
    title = models.CharField(
        max_length=256, help_text=_("A short descriptive title.")
    )
    slug = models.SlugField(
        max_length=256, db_index=True, unique=True
    )
    success_message = models.CharField(max_length=256, blank=True, null=True)
    failure_message = models.CharField(max_length=256, blank=True, null=True)
    redirect_to = models.CharField(
        max_length=256, blank=True, null=True,
        help_text="URL to which this form will redirect to after processesing."
    )

    class Meta(object):
        abstract = True


class Form(BaseFormModel):
    """Form model which encompasses a set of form fields and defines an action
    when the form processed.
    """
    actions = models.ManyToManyField(Action, through=FormActionThrough)

    class Meta(object):
        ordering = ["title"]

    def __unicode__(self):
        return self.title

    def absolute_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return reverse("formfactory:form-detail", kwargs={"slug": self.slug})

    def as_form(self, data=None, files=None):
        """
        Builds the form factory object and returns it.
        """
        if not self.pk:
            raise AttributeError(
                "The model needs to be saved before a form can be generated."
            )

        return factory.FormFactory(
            data, files, prefix=self.slug, field_groups=self.fieldgroups.all(),
            form_id=self.pk, actions=self.actions.all()
        )


class Wizard(BaseFormModel):
    """
    Wizard model that groups forms together.
    """
    actions = models.ManyToManyField(Action, through="WizardActionThrough")
    forms = models.ManyToManyField(Form, through="WizardFormThrough")

    def absolute_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return reverse("formfactory:wizard-detail", kwargs={"slug": self.slug})


class WizardFormThrough(models.Model):
    """Through table for forms to wizards which defines an order.
    """
    wizard = models.ForeignKey(Wizard)
    form = models.ForeignKey(Form)
    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]
        verbose_name = "Form"
        verbose_name_plural = "Forms"

    def __unicode__(self):
        return "%s (%s)" % (self.form.title, self.order)


class WizardActionThrough(models.Model):
    """Through table for wizard actions with a defined order.
    """
    action = models.ForeignKey(Action)
    wizard = models.ForeignKey(Wizard)
    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]
        verbose_name = "Wizard Action"
        verbose_name_plural = "Wizard Actions"

    def __unicode__(self):
        return "%s (%s)" % (self.action.action, self.order)


class FieldChoice(models.Model):
    """Defines options for select or multiselect field types.
    """
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    class Meta(object):
        ordering = ["label"]

    def __unicode__(self):
        return "%s:%s" % (self.label, self.value)


class FormFieldGroup(models.Model):
    """Enable the grouping of fields and how that field should be rendered.
    """
    title = models.CharField(
        max_length=256, help_text=_("A short descriptive title.")
    )
    forms = models.ManyToManyField(
        Form, through="FieldGroupFormThrough", related_name="fieldgroups"
    )

    def __unicode__(self):
        return self.title


class FieldGroupFormThrough(models.Model):
    """Through table for field groups forms with a defined order.
    """
    field_group = models.ForeignKey(FormFieldGroup)
    form = models.ForeignKey(Form)
    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]
        verbose_name = "Form"
        verbose_name_plural = "Forms"

    def __unicode__(self):
        return "%s (%s)" % (self.field_group.title, self.order)


class FormField(models.Model):
    """Defines a form field with all options and required attributes.
    """
    title = models.CharField(
        max_length=256, help_text=_("A short descriptive title.")
    )
    slug = models.SlugField(
        max_length=256, db_index=True, unique=True
    )
    field_groups = models.ManyToManyField(
        FormFieldGroup, through="FieldGroupThrough", related_name="fields"
    )
    field_type = models.CharField(choices=FIELD_TYPES, max_length=128)
    widget = models.CharField(
        choices=WIDGET_TYPES, max_length=128, blank=True, null=True,
        help_text=_("Leave blank if you prefer to use the default widget.")
    )
    label = models.CharField(max_length=64, blank=True, null=True)
    initial = models.TextField(blank=True, null=True)
    max_length = models.PositiveIntegerField(
        default=256, blank=True, null=True
    )
    help_text = models.CharField(max_length=256, blank=True, null=True)
    placeholder = models.CharField(max_length=128, blank=True, null=True)
    required = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)
    choices = models.ManyToManyField(FieldChoice, blank=True, null=True)
    additional_validators = models.CharField(
        choices=ADDITIONAL_VALIDATORS, max_length=128, blank=True, null=True
    )

    def __unicode__(self):
        return self.title


class FieldGroupThrough(models.Model):
    """Through table for form fields and field groups with a defined order.
    """
    field = models.ForeignKey(FormField)
    field_group = models.ForeignKey(FormFieldGroup)
    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]
        verbose_name = "Field Group"
        verbose_name_plural = "Field Groups"

    def __unicode__(self):
        return "%s (%s)" % (self.field.title, self.order)
