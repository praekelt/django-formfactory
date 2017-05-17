from os import path

from django.conf import settings
from django.utils.module_loading import import_module


def clean_key(func):
    """Provides a clean, readable key from the funct name and module path.
    """
    module = func.__module__.replace("formfactoryapp.", "")
    return "%s.%s" % (module, func.__name__)


def auto_registration(func_type):
    for app_name in settings.INSTALLED_APPS:
        try:
            import_module("%s.formfactoryapp.%s" % (app_name, func_type))
        except ImportError:
            pass


def get_label(form_instance, field_name):
    return form_instance.fields[field_name].label


def get_all_model_fields(model):
    return model._meta.get_all_field_names()


def set_file_name(file_path, count):
    file_name, extension = path.splitext(file_path)
    if count:
        return "%s_%s%s" % (file_name, count, extension)
    return file_path


def increment_file_name(file_path):
    count = 0
    while path.exists(set_file_name(file_path, count)):
        count += 1
    return set_file_name(file_path, count)
