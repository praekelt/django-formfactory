from django.conf import settings


SETTINGS = getattr(settings, "FORMFACTORY", {
    "field-types": [
        "BooleanField", "CharField", "ChoiceField", "DateField",
        "DateTimeField", "DecimalField", "EmailField", "FileField",
        "FloatField", "GenericIPAddressField", "IntegerField",
        "MultipleChoiceField", "SlugField", "SplitDateTimeField", "TimeField",
        "URLField", "UUIDField"
    ],
    "widget-types": [
        "CheckboxInput", "CheckboxSelectMultiple", "DateInput",
        "DateTimeInput", "EmailInput", "FileInput", "HiddenInput",
        "NullBooleanSelect", "NumberInput", "PasswordInput", "RadioSelect",
        "Select", "SelectMultiple", "Textarea", "TextInput", "TimeInput",
        "URLInput"
    ],
    "error-types": [
        "required",
    ],
    "redirect-url-param-name": "next"
})


_registry = {
    "actions": {},
    "validators": {}
}
