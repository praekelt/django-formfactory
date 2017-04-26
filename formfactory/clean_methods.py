from formfactory import _registry
from formfactory.utils import auto_registration, clean_key


def register(func):
    key = clean_key(func)
    _registry["clean_methods"][key] = func

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def unregister(func):
    key = clean_key(func)
    if key in _registry["clean_methods"]:
        del _registry["clean_methods"][key]


def get_registered_clean_methods():
    return _registry["clean_methods"]


def auto_discover():
    """Perform discovery of action functions over all other installed apps.
    """
    auto_registration("clean_methods")
