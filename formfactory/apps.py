from django.apps import AppConfig, apps
from django.utils.module_loading import import_module


class FormFactoryAppConfig(AppConfig):
    name = "formfactory"

    def ready(self):
        """Initially import formfactories default actions and than perform
        discovery on all other installed apps
        """
        from formfactory import actions

        for app in apps.get_app_configs():
            try:
                import_module("%s.formfactoryapp.actions" % app.name)
            except ImportError:
                pass
