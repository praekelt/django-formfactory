from django import forms
from django.utils.translation import ugettext_lazy as _

from formfactory import models


class FormAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.Form
        fields = [
            "title", "slug", "success_message", "failure_message",
            "redirect_to", "submit_button_text", "enable_csrf",
            "ajax_post", "clean_method"
        ]


class ActionAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.Action
        fields = ["action"]


class ActionParamAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.ActionParam
        fields = ["key", "value"]


class FormActionThroughAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.FormActionThrough
        fields = ["action", "form", "order"]


class ValidatorAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.Validator
        fields = ["validator"]


class CleanMethodAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.CleanMethod
        fields = ["clean_method"]


class CustomErrorAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.CustomErrorMessage
        fields = ["key", "value"]


class CustomErrorInlineAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.FormFieldErrorMessageProxy
        fields = ["formfield", "customerrormessage"]
        labels = {
            "customerrormessage": _("Error message"),
        }


class FormDataAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.FormData
        fields = ["uuid", "form"]


class FormDataItemAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.FormDataItem
        fields = ["form_data", "form_field", "value"]


class FormActionParamAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.ActionParam
        fields = ["key", "value"]


class WizardAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.Wizard
        fields = ["title", "slug", "redirect_to"]


class WizardFormThroughAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.WizardFormThrough
        fields = ["wizard", "form", "order"]


class WizardActionThroughAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.WizardActionThrough
        fields = ["action", "wizard", "order"]


class FormFieldGroupAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.FormFieldGroup
        fields = ["title", "show_title", "forms"]


class FieldGroupFormThroughAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.FieldGroupFormThrough
        fields = ["form", "field_group", "order"]


class FieldGroupThroughAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.FieldGroupThrough
        fields = ["field_group", "field", "order"]


class FieldChoiceAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.FieldChoice
        fields = ["label", "value"]


class FormFieldAdminForm(forms.ModelForm):
    class Meta(object):
        model = models.FormField
        fields = [
            "title", "slug", "field_groups", "field_type", "widget", "label",
            "initial", "max_length", "help_text", "placeholder", "required",
            "disabled", "choices", "model_choices_content_type",
            "model_choices_object_id", "additional_validators",
            "error_messages", "paragraph"
        ]


class EmptyForm(forms.Form):
    pass
