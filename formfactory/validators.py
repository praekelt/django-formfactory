from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from formfactory import _registery


def register(kls):
    _registery["validators"][kls.__name__] = kls


def unregister(kls):
    if kls in _registery["validators"].values():
        del _registery["validators"][kls.__name__]


def get_registered_validators():
    return _registery["validators"]


class MetaClass(type):
    def __new__(mcs, clsname, bases, attrs):
        newclass = super(MetaClass, mcs).__new__(mcs, clsname, bases, attrs)
        register(newclass)
        return newclass


class BaseValidator(object):
    __metaclass__ = MetaClass

    validation_message = "%(value)s did not validate"

    def condition(self, value):
        raise NotImplementedError()

    def validate(self, value):
        if not self.condition(value):
            raise ValidationError(
                _(self.validation_message), params={"value": value},
            )
        return True
