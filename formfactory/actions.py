from django.core.mail import send_mail

from formfactory import _registry, SETTINGS
from formfactory.utils import auto_registration, clean_key


def register(func):
    key = clean_key(func)
    _registry["actions"][key] = func

    def wrapper(*args):
        return func(*args)
    return wrapper


def unregister(func):
    key = clean_key(func)
    if key in _registry["actions"]:
        del _registry["actions"][key]


def get_registered_actions():
    return _registry["actions"]


def auto_discover():
    """Perform discovery of action functions over all other installed apps.
    """
    auto_registration("actions")


@register
def store_data(form_instance):
    """An action which store submitted form data in a simple key/value store.
    """
    from formfactory.models import FormData, FormDataItem

    cleaned_data = form_instance.cleaned_data
    form_data = FormData.objects.create(
        uuid=cleaned_data.pop("uuid"),
        form_id=cleaned_data.pop("form_id"),
    )
    for key, value in cleaned_data.items():
        FormDataItem.objects.create(
            form_data=form_data,
            form_field_id=form_instance.fields[key].field_pk,
            value=value
        )


@register
def send_email(form_instance):
    """An action which sends a plain text email with all submitted data.
    A subject and to field must be provided.
    """
    cleaned_data = form_instance.cleaned_data

    action_settings = SETTINGS.get("email-action", {})
    from_email = action_settings["from-email"]
    try:
        to_email = cleaned_data.pop(action_settings["to-field"])
    except KeyError:
        raise KeyError("No to email field name setting provided.")
    try:
        subject = cleaned_data.pop(action_settings["subject-field"])
    except KeyError:
        raise KeyError("No subject field name setting provided.")

    email_body = [
        "%s: %s\n\r" % (label, value) for label, value in cleaned_data.items()
    ]
    send_mail(subject, email_body, from_email, [to_email])
