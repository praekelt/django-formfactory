from formfactory import _registery


def register(kls):
    validators = _registery.setdefault("validators", [])
    validators.append(kls)
