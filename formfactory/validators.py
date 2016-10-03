from formfactory import _registry
from formfactory.utils import clean_key


def register(func):
    key = clean_key(func)
    _registry["validators"][key] = func

    def wrapper(*args):
        return func(*args)
    return wrapper


def unregister(func):
    key = clean_key(func)
    if key in _registry["validators"]:
        del _registry["validators"][key]


def get_registered_validators():
    return _registry["validators"]
