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
        "empty", "incomplete", "invalid", "invalid_choice", "invalid_image",
        "invalid_list", "invalid_date", "invalid_time", "invalid_pk_value",
        "list", "max_decimal_places", "max_digits", "max_length", "max_value",
        "max_whole_digits", "min_length", "min_value", "missing", "required",
    ],
    "redirect-url-param-name": "next"
})


_registry = {
    "actions": {},
    "validators": {},
    "clean_methods": {}
}
