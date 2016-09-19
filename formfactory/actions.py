from formfactory import _registery


def register(kls):
    validators = _registery.setdefault("actions", [])
    actions.append(kls)
