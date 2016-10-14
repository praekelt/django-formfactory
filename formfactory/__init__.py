from django.conf import settings


SETTINGS = getattr(settings, "FORMFACTORY", {
    "field-types": [
        "BooleanField", "CharField", "ChoiceField", "DateField",
        "DateTimeField", "DecimalField", "EmailField", "FloatField",
        "GenericIPAddressField", "IntegerField", "MultipleChoiceField",
        "SlugField", "SplitDateTimeField", "TimeField", "URLField", "UUIDField"
    ],
    "widget-types": [
        "TextInput", "NumberInput", "EmailInput", "URLInput", "PasswordInput",
        "HiddenInput", "DateInput", "DateTimeInput", "TimeInput",
        "Textarea", "CheckboxInput", "Select", "NullBooleanSelect",
        "SelectMultiple", "RadioSelect", "CheckboxSelectMultiple"
    ],
    "redirect-url-param-name": "next"
})


_registry = {
    "actions": {},
    "validators": {}
}
