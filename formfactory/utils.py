from django.apps import apps
from django.utils.module_loading import import_module


def clean_key(func):
    """Provides a clean, readable key from the funct name and module path.
    """
    module = func.__module__.replace("formfactoryapp.", "")
    return "%s.%s" % (module, func.__name__)


def auto_registration(func_type):
    for app in apps.get_app_configs():
        try:
            import_module("%s.formfactoryapp.%s" % (app.name, func_type))
        except ImportError:
            pass
