from django.apps import AppConfig, apps
from django.utils.module_loading import import_module


class FormFactoryAppConfig(AppConfig):
    name = "formfactory"

    def ready(self):
        for app in apps.get_app_configs():
            try:
                import_module("%s.actions" % app.name)
            except ImportError:
                print "No action found", app.name
