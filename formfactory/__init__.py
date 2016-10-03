from django.conf import settings


default_app_config = "formfactory.apps.FormFactoryAppConfig"


SETTINGS = getattr(settings, "FORMFACTORY", {
    "field-types": [
        "BooleanField", "CharField", "ChoiceField", "DateField",
        "DateTimeField", "DecimalField", "EmailField", "FloatField",
        "GenericIPAddressField", "IntegerField", "MultipleChoiceField",
        "SlugField", "SplitDateTimeField", "TimeField", "URLField", "UUIDField"
    ],
    "email-action": {
        "from-email": settings.DEFAULT_FROM_EMAIL,
        "to-field": "send-to",
        "subject-field": "email-subject"
    }
})


_registry = {
    "actions": {},
    "validators": {}
}
