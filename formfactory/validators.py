from formfactory import _registery


def register(kls):
    validators = _registery.setdefault("validators", [])
    validators.append(kls)


def unregister(kls):
    validators = _registery.setdefault("validators", [])
    if kls in validators:
        validators.remove(kls)
