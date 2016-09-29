from formfactory import _registry


def register(func):
    key = "%s.%s" % (func.__module__, func.__name__)
    _registry["validators"][key] = func

    def wrapper(*args):
        return func(*args)
    return wrapper


def unregister(func):
    key = "%s.%s" % (func.__module__, func.__name__)
    if key in _registry["validators"]:
        del _registry["validators"][key]


def get_registered_validators():
    return _registry["validators"]
