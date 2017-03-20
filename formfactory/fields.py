from django.forms.fields import Field, CharField, BooleanField
from django.apps import apps
from django.utils.module_loading import import_module

from formfactory import _registry


def auto_discover():
    """Perform discovery of custom fields
    """
    for app in apps.get_app_configs():
        try:
            module = import_module("%s.formfactoryapp.%s" % (app.name, "fields"))
            # print "================== ", module
            get_form_fields(module)
        except ImportError:
            pass


def get_form_fields(module):
    """Get all form fields defined in this module.
     Form fields should be a subclass of django.forms.fields.Field
    """
    for name in dir(module):
        try:
            if issubclass(getattr(module, name), Field):
                _registry["fields"][name] = getattr(module, name)
        except TypeError:
            pass


def get_registered_fields():
    return _registry["fields"]
