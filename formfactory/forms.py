from django import forms

from formfactory import models


class FormAdminForm(forms.ModelForm):
    class Meta:
        model = models.Form
        fields = ["title", "slug"]


class FormActionThroughAdminForm(forms.ModelForm):
    class Meta:
        model = models.FormActionThrough
        fields = ["action", "form", "order"]


class FieldChoiceAdminForm(forms.ModelForm):
    class Meta:
        model = models.FieldChoice
        fields = ["label", "value"]


class FormFieldAdminForm(forms.ModelForm):
    class Meta:
        model = models.FormField
        fields = [
            "title", "position", "form", "field_type", "label", "initial",
            "label", "required", "disabled", "choices", "additional_validators"
        ]
