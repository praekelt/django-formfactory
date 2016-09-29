from django.conf import settings


default_app_config = "formfactory.apps.FormFactoryAppConfig"


SETTINGS = getattr(settings, "FORMFACTORY", {
    "field-types": [
        "BooleanField", "CharField", "ChoiceField", "DateField",
        "DateTimeField", "DecimalField", "EmailField", "FloatField",
        "GenericIPAddressField", "IntegerField", "MultipleChoiceField",
        "SlugField", "SplitDateTimeField", "TimeField", "URLField", "UUIDField"
    ]
})


_registry = {
    "actions": {},
    "validators": {}
}
