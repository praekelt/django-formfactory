from django.apps import AppConfig, apps
from django.utils.module_loading import import_module


class FormFactoryAppConfig(AppConfig):
    name = "formfactory"

    def ready(self):
        """Initially import formfactories default actions and validators, than
        perform discovery on all other installed apps.
        """
        for app in apps.get_app_configs():
            try:
                import_module("%s.formfactoryapp.actions" % app.name)
            except ImportError:
                pass
            try:
                import_module("%s.formfactoryapp.validators" % app.name)
            except ImportError:
                pass
