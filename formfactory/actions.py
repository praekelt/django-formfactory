from formfactory import _registery


def register(kls):
    actions = _registery.setdefault("actions", [])
    actions.append(kls)


def unregister(kls):
    actions = _registery.setdefault("actions", [])
    if kls in actions:
        actions.remove(kls)
