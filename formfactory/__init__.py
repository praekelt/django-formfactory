from django.conf import settings


SETTINGS = getattr(settings, "FORMFACTORY", {})

_registery = {}
