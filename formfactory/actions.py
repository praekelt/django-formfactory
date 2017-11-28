import os

from django.conf import settings
from django.contrib import auth
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail

from formfactory import _registry, exceptions
from formfactory.utils import (
    auto_registration, clean_key, get_label, increment_file_name
)


def register(func):
    key = clean_key(func)
    _registry["actions"][key] = func

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
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
def store_data(form_instance, **kwargs):
    """An action which store submitted form data in a simple key/value store.
    """
    from formfactory.models import FormData, FormDataItem

    cleaned_data = form_instance.cleaned_data
    form_data = FormData.objects.create(
        uuid=cleaned_data.pop("uuid"),
        form_id=cleaned_data.pop("form_id"),
    )

    # Formfactory can end up in a scenario where a none required field gets to
    # this stage as empty in the cleaned data. However the actual data field
    # that is being saved to is required and not null. At this stage seems to
    # only happen with wizards. Solution: if the field is not required and the
    # value is not present pop it from the dict that will be saved.
    for name, field in form_instance.fields.items():
        if not field.required and not cleaned_data.get(name, None):
            cleaned_data.pop(name)

    for key, value in cleaned_data.items():
        FormDataItem.objects.create(
            form_data=form_data,
            form_field_id=form_instance.fields[key].field_pk,
            value=value
        )


@register
def send_email(form_instance, **kwargs):
    """An action which sends a plain text email with all submitted data.
    A subject and to field must be provided.
    """
    cleaned_data = form_instance.cleaned_data

    try:
        from_email = cleaned_data.pop(kwargs["from_email_field"])
    except KeyError:
        raise exceptions.MissingActionParam("send_email", "from_email_field")
    try:
        to_email = cleaned_data.pop(kwargs["to_email_field"])
    except KeyError:
        raise exceptions.MissingActionParam("send_email", "to_email_field")
    try:
        subject = cleaned_data.pop(kwargs["subject_field"])
    except KeyError:
        raise exceptions.MissingActionParam("send_email", "subject_field")

    if "uuid" in cleaned_data:
        del cleaned_data["uuid"]

    if "form_id" in cleaned_data:
        del cleaned_data["form_id"]

    email_body = "".join([
        "%s: %s\n\r" % (get_label(form_instance, label), value)
        for label, value in cleaned_data.items()
    ])
    send_mail(subject, email_body, from_email, [to_email])


@register
def login(form_instance, **kwargs):
    """An action which authenticates and logs a user in using the django auth
    framework.
    """
    cleaned_data = form_instance.cleaned_data

    try:
        username = cleaned_data.pop(kwargs["username_field"])
    except KeyError:
        raise exceptions.MissingActionParam("login", "username_field")
    try:
        password = cleaned_data.pop(kwargs["password_field"])
    except KeyError:
        raise exceptions.MissingActionParam("login", "password_field")

    request = kwargs.get("request")
    user = auth.authenticate(
        request=request, username=username, password=password, **cleaned_data
    )
    if user is not None:
        auth.login(request, user)


@register
def file_upload(form_instance, **kwargs):
    """An action which uploads all files to a specific location.
    """
    cleaned_data = form_instance.cleaned_data

    file_objects = [
        f for f in cleaned_data.values() if isinstance(f, InMemoryUploadedFile)
    ]

    try:
        upload_path = cleaned_data.pop(kwargs["upload_path_field"])
    except KeyError:
        raise exceptions.MissingActionParam("file_upload", "upload_path_field")

    full_upload_path = os.path.join(settings.MEDIA_ROOT, upload_path)

    # Creates the dir path if it does not already exist
    if not os.path.exists(full_upload_path):
        os.makedirs(full_upload_path)

    for file_object in file_objects:
        file_path = increment_file_name(
            os.path.join(full_upload_path, file_object.name)
        )
        with open(file_path, "wb+") as destination:
            for chunk in file_object.chunks():
                destination.write(chunk)
