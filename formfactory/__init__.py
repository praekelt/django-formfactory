from django.conf import settings


# TODO add contenttype settings in
SETTINGS = getattr(settings, "FORMFACTORY", {
    "field-types": [
        "BooleanField", "CharField", "ChoiceField", "DateField",
        "DateTimeField", "DecimalField", "EmailField", "FileField",
        "FloatField", "GenericIPAddressField", "IntegerField",
        "MultipleChoiceField", "SlugField", "SplitDateTimeField", "TimeField",
        "URLField", "UUIDField", "ParagraphField"
    ],
    "widget-types": [
        "CheckboxInput", "CheckboxSelectMultiple", "DateInput",
        "DateTimeInput", "EmailInput", "FileInput", "HiddenInput",
        "NullBooleanSelect", "NumberInput", "PasswordInput", "RadioSelect",
        "Select", "SelectMultiple", "Textarea", "TextInput", "TimeInput",
        "URLInput", "ParagraphWidget"
    ],
    "error-types": [
        "empty", "incomplete", "invalid", "invalid_choice", "invalid_image",
        "invalid_list", "invalid_date", "invalid_time", "invalid_pk_value",
        "list", "max_decimal_places", "max_digits", "max_length", "max_value",
        "max_whole_digits", "min_length", "min_value", "missing", "required",
    ],
    "redirect-url-param-name": "next",
    "allowed-extra-widget-attrs": [
        "safe_paragraph",
    ]
})


_registry = {
    "actions": {},
    "validators": {},
    "clean_methods": {}
}
