from django import forms

from formfactory import clean_methods


@clean_methods.register
def check_if_values_match(form_instance, **kwargs):
    """Clean method for when a contact updates password.
    """
    first_field = form_instance.cleaned_data["first_field"]
    second_field = form_instance.cleaned_data["second_field"]

    if not first_field == second_field:
        raise forms.ValidationError(
            "The values you entered are not equal."
        )
