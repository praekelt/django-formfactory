from formfactory import _registry

from formfactory.models import FormData, FormDataItem


def register(func):
    _registry["actions"][func.__name__] = func


def unregister(kls):
    if kls in _registry["actions"].values():
        del _registry["actions"][kls.__name__]


def get_registered_actions():
    return _registry["actions"]


def store_data(form_instance):
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

register(store_data)
