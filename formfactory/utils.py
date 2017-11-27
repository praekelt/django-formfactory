from os import path

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


def get_label(form_instance, field_name):
    return form_instance.fields[field_name].label


def get_all_model_fields(model):
    return [field.name for field in model._meta.get_fields()]


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


def order_by_through(queryset, through_model_name, filter_on,
        filter_instance, ordered_object_type, order_by="order"):
    """
    Helps with an issue in django 1.9 and 1.9.1 that can be found here:
    https://code.djangoproject.com/ticket/26092
    :return: ordered QuerySet
    """

    return_set = None
    try:
        return_set = queryset.order_by(
            through_model_name.lower()
        )

        # Make an arb call on the list to trigger the potential error.
        len(return_set)
    except AttributeError as e:

        # Models can't be imported when utils first initialises.
        from formfactory import models
        model = getattr(models, through_model_name)
        filter_data = {filter_on: filter_instance}
        return_set = [getattr(instance, ordered_object_type)
            for instance
            in model.objects.filter(
                **filter_data
            ).order_by(order_by)
        ]
    return return_set
