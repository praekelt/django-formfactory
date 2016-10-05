from formfactory import _registry
from formfactory.utils import auto_registration, clean_key


def register(func):
    key = clean_key(func)
    _registry["validators"][key] = func

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def unregister(func):
    key = clean_key(func)
    if key in _registry["validators"]:
        del _registry["validators"][key]


def get_registered_validators():
    return _registry["validators"]


def auto_discover():
    """Perform discovery of validator functions over all other installed apps.
    """
    auto_registration("validators")
