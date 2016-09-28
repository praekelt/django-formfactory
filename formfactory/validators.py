from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from formfactory import _registery


_validators = _registery.setdefault("validators", {})


def register(kls):
    _validators[kls.__class__.__name__] = kls


def unregister(kls):
    if kls in _validators:
        del _validators[kls.__class__.__name__]


def get_registered_validators():
    return _validators


class BaseValidator(object):
    validation_message = "%(value)s did not validate"

    def condition(self, value):
        raise NotImplementedError()

    def validate(self, value):
        if not self.condition(value):
            raise ValidationError(
                _(self.validation_message), params={"value": value},
            )
        return True
