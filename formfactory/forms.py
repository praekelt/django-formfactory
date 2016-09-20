from django import forms

from formfactory.models import FieldChoice, Form, FormField


class FormAdminForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ["title", "slug", "action"]


class FieldChoiceAdminForm(forms.ModelForm):
    class Meta:
        model = FieldChoice
        fields = ["label", "value"]


class FormFieldAdminForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = [
            "title", "position", "form", "field_type", "label", "initial",
            "label", "required", "disabled", "choices", "additional_validators"
        ]
