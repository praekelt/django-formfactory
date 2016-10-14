from django.conf import settings


SETTINGS = getattr(settings, "FORMFACTORY", {
    "field-types": [
        "BooleanField", "CharField", "ChoiceField", "DateField",
        "DateTimeField", "DecimalField", "EmailField", "FloatField",
        "GenericIPAddressField", "IntegerField", "MultipleChoiceField",
        "SlugField", "SplitDateTimeField", "TimeField", "URLField", "UUIDField"
    ],
    "redirect-url-param-name": "next"
})


_registry = {
    "actions": {},
    "validators": {}
}
