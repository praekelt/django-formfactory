from formfactory import _registery
from formfactory.models import FormData, FormDataItems


def register(kls):
    _registery["actions"][kls.__name__] = kls


def unregister(kls):
    if kls in _registery["actions"].values():
        del _registery["actions"][kls.__name__]


def get_registered_actions():
    return _registery["actions"]


class BaseAction(object):
    def run(self, form_instance):
        raise NotImplementedError()


class StoreAction(BaseAction):
    """Stores the data to a simple key value store, grouped by a unique uuid per
    submition.
    """
    def run(self, form_instance):
        cleaned_data = form_instance.cleaned_data
        form_data = FormData.objects.create(
            uuid=cleaned_data["uuid"],
            form_id=cleaned_data["form_id"],
        )
        for key, value in cleaned_data.items():
            FormDataItems.objects.create(
                form_data=form_data,
                form_field_id=form_instance.fields[key].pk,
                value=value
            )


class EmailAction(BaseAction):
    def run(self, form_instance):
        pass


register(StoreAction)
