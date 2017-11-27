import importlib
import markdown

from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import mark_safe
from django.utils.translation import ugettext as _

from simplemde.fields import SimpleMDEField

from formfactory import (
    _registry, actions, clean_methods, factory, SETTINGS, validators, utils
)


actions.auto_discover()
validators.auto_discover()
clean_methods.auto_discover()


def _FIELD_TYPES():
    fields = ()
    for content_type, field in SETTINGS["field-types"]:
        module = importlib.import_module(content_type.replace(".%s" % field, ""))
        if issubclass(getattr(module, field), forms.fields.Field):
            fields = fields + ((content_type, field),)
    return fields

FIELD_TYPES = _FIELD_TYPES()

def _WIDGET_TYPES():
    widgets = ()
    for content_type, widget in SETTINGS["widget-types"]:
        module = importlib.import_module(content_type.replace(".%s" % widget, ""))
        if issubclass(getattr(module, widget), forms.widgets.Widget):
            widgets = widgets + ((content_type, widget),)
    return widgets

WIDGET_TYPES = _WIDGET_TYPES()

ERROR_MESSAGES = tuple(
    (error_type, error_type) for error_type in SETTINGS["error-types"]
)

ADDITIONAL_VALIDATORS = tuple(
    (validator, validator)
    for validator in validators.get_registered_validators()
)

FORM_ACTIONS = tuple(
    (action, action) for action in actions.get_registered_actions()
)

CLEAN_METHODS = tuple(
    (clean, clean) for clean in clean_methods.get_registered_clean_methods()
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


class Validator(models.Model):
    """Defines a form field validator.
    """
    validator = models.CharField(choices=ADDITIONAL_VALIDATORS, max_length=128)

    def __unicode__(self):
        return self.validator

    @property
    def as_function(self):
        return _registry["validators"][self.validator]


class CleanMethod(models.Model):
    """Defines a form's clean method.
    """
    clean_method = models.CharField(choices=CLEAN_METHODS, max_length=128)

    def __unicode__(self):
        return self.clean_method

    @property
    def as_function(self):
        return _registry["clean_methods"][self.clean_method]


class CustomErrorMessage(models.Model):
    key = models.CharField(choices=ERROR_MESSAGES, max_length=128)
    value = models.CharField(max_length=256)

    class Meta(object):
        verbose_name = "Field error message"
        verbose_name_plural = "Field error messages"

    def __unicode__(self):
        return "%s: %s" % (self.key, self.value)


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
    clean_method = models.ForeignKey(CleanMethod, blank=True, null=True)
    submit_button_text = models.CharField(
        max_length=64, default="Submit",
        help_text="The text you would like on the form submit button."
    )
    enable_csrf = models.BooleanField(
        _("Enable CSRF protection"),
        default=True,
        help_text=_("""Cross site request forgery protection may not be needed \
in all cases. Since it incurs a performance penalty you may wish to disable \
it.""")
    )
    ajax_post = models.BooleanField(
        _("Enable AJAX posting."),
        default=False,
        help_text=_("Hook for default submit handler to be overriden by JS.")
    )

    class Meta(object):
        ordering = ["title"]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.enable_csrf:
            return reverse(
                "formfactory:form-detail", kwargs={"slug": self.slug}
            )
        else:
            return reverse(
                "formfactory:form-detail-nocsrf", kwargs={"slug": self.slug}
            )

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    def as_form(self, **kwargs):
        """
        Builds the form factory object and returns it.
        """
        if not self.pk:
            raise AttributeError(
                "The model needs to be saved before a form can be generated."
            )

        ordered_field_groups = utils.order_by_through(
            self.fieldgroups.all(),
            "FieldGroupFormThrough",
            "form",
            self,
            "field_group"
        )
        kwargs.update({
            "field_groups": ordered_field_groups,
            "form_id": self.pk,
            "actions": self.actions.all(),
            "prefix": kwargs.get("prefix", self.slug),
            "clean_method": self.clean_method
        })

        return factory.FormFactory(**kwargs)


class Wizard(BaseFormModel):
    """
    Wizard model that groups forms together.
    """
    actions = models.ManyToManyField(Action, through="WizardActionThrough")
    forms = models.ManyToManyField(Form, through="WizardFormThrough")

    def __unicode__(self):
        return self.title

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
    show_title = models.BooleanField(
        default=False,
        help_text=_("Select this for Field group title to be displayed.")
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
        verbose_name = "Field Group"
        verbose_name_plural = "Field Groups"

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
    label = models.CharField(max_length=256, blank=True, null=True)
    initial = models.TextField(blank=True, null=True)
    max_length = models.PositiveIntegerField(
        default=256, blank=True, null=True
    )
    help_text = models.CharField(max_length=256, blank=True, null=True)
    placeholder = models.CharField(max_length=128, blank=True, null=True)
    required = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)
    choices = models.ManyToManyField(FieldChoice, blank=True)
    model_choices_content_type = models.ForeignKey(
        ContentType, blank=True, null=True
    )
    model_choices_object_id = models.PositiveIntegerField(
        blank=True, null=True
    )
    model_choices = GenericForeignKey(
        "model_choices_content_type", "model_choices_object_id"
    )
    additional_validators = models.ManyToManyField(Validator, blank=True)
    error_messages = models.ManyToManyField(CustomErrorMessage, blank=True)
    paragraph = SimpleMDEField(
        null=True,
        blank=True,
        help_text="Markdown for the formfactory ParagraphField and"\
        " ParagraphWidget combination."
    )

    def __unicode__(self):
        return self.title

    @property
    def get_field_meta(self):
        """
        Return field meta info
        :return: tuple(module, field_class_name)
        """
        for content_type, field in FIELD_TYPES:
            if self.field_type == content_type:
                module = importlib.import_module(
                    content_type.replace(".%s" % field, "")
                )
                return (module, field)
        raise Exception("Field; %s on Field model %s: Does not have a" \
            "properly defined content_type value" % (self.field_type, self.id))

    @property
    def get_widget_meta(self):
        """
        Return field meta info
        :return: tuple(module, widget_class_name)
        """
        for content_type, widget in WIDGET_TYPES:
            if self.widget == content_type:
                module = importlib.import_module(
                    content_type.replace(".%s" % widget, "")
                )
                return (module, widget)
        raise Exception("Widget; %s on Field model %s: Does not have a " \
            "properly defined content_type value" % (self.widget, self.id))

    @property
    def safe_paragraph(self):
        if self.paragraph:
            return mark_safe(markdown.markdown(self.paragraph))
        else:
            return self.paragraph


class FieldGroupThrough(models.Model):
    """Through table for form fields and field groups with a defined order.
    """
    field = models.ForeignKey(FormField)
    field_group = models.ForeignKey(FormFieldGroup)
    order = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["order"]
        verbose_name = "Field"
        verbose_name_plural = "Fields"

    def __unicode__(self):
        return "%s (%s)" % (self.field.title, self.order)


class FormFieldErrorMessageProxy(FormField.error_messages.through):
    class Meta:
        auto_created = True
        proxy = True

    def __unicode__(self):
        return str(self.customerrormessage)


class FormFieldValidatorProxy(FormField.additional_validators.through):
    class Meta:
        auto_created = True
        proxy = True

    def __unicode__(self):
        return str(self.validator)
