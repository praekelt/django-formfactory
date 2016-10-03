from django import forms

from formfactory import models


class FormAdminForm(forms.ModelForm):
    class Meta:
        model = models.Form
        fields = ["title", "slug"]


class ActionForm(forms.ModelForm):
    class Meta:
        model = models.Action
        fields = ["action"]


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
            "title", "slug", "position", "form", "field_type", "label",
            "initial", "label", "required", "disabled", "choices",
            "additional_validators"
        ]


class FormDataAdminForm(forms.ModelForm):
    class Meta:
        model = models.FormData
        fields = ["uuid", "form"]


class FormDataItemAdminForm(forms.ModelForm):
    class Meta:
        model = models.FormDataItem
        fields = ["form_data", "form_field", "value"]
