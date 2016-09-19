from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from formfactory import _registery


_validators = _registery.setdefault("validators", [])


def register(kls):
    _validators.append(kls)


def unregister(kls):
    if kls in _validators:
        _validators.remove(kls)


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





"""
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
"""
