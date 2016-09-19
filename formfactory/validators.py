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
    pass
