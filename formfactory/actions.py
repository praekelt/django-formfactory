from formfactory import _registery


_actions = _registery.setdefault("actions", [])


def register(kls):
    _actions.append(kls)

def unregister(kls):
    _actions = _registery.setdefault("actions", [])
    if kls in _actions:
        _actions.remove(kls)

def get_registered_actions():
    return _actions


class BaseAction(object):
    def run(self, value):
        raise NotImplementedError()
