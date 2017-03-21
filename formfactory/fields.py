from django.apps import apps
from django.forms.fields import Field
from django.utils.module_loading import import_module

from formfactory import _registry, SETTINGS

# Keys for fields registered in _registry["fields"] are suffixed.
# This constant is used for convenience in  getting the django
# built-in fields.
DJANGO_FIELDS_MODULE = "django.forms.fields"


def auto_discover():
    """Perform discovery of custom fields, starting with the
    built-in django fields.
    """
    module = import_module(DJANGO_FIELDS_MODULE)
    get_form_fields(module)

    for app in apps.get_app_configs():
        try:
            module = import_module("%s.formfactoryapp.%s" % (app.name, "fields"))
            get_form_fields(module)
        except ImportError:
            pass

    # remove blacklisted django built-in fields
    remove_excluded_fields()


def formatted_field_key(field_name, suffix):
    """Returns a key in the format it will be stored in
     _registry["fields"], i.e. 'field_name-suffix'
    """
    return "{}-{}".format(field_name, suffix)


def get_form_fields(module):
    """Get all form fields defined in this module.
     Form fields should be a subclass of django.forms.fields.Field
    """
    for name in dir(module):
        try:
            if issubclass(getattr(module, name), Field):
                field_class = getattr(module, name)
                key = formatted_field_key(
                    field_class.__name__, field_class.__module__
                )
                _registry["fields"][key] = field_class
        except TypeError:
            pass


def remove_excluded_fields():
    """Remove fields listed in settings.FORMFACTORY['excluded_fields']
    """
    for field_name in SETTINGS["excluded_fields"]:
        _registry["fields"].pop(
            formatted_field_key(field_name, DJANGO_FIELDS_MODULE)
        )


def get_registered_fields():
    return _registry["fields"]
