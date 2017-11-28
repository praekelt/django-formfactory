from django.conf import settings


SETTINGS = getattr(settings, "FORMFACTORY", {
    "field-types": [
            ("django.forms.fields.BooleanField", "BooleanField"),
            ("django.forms.fields.CharField", "CharField"),
            ("django.forms.fields.ChoiceField", "ChoiceField"),
            ("django.forms.fields.DateField", "DateField"),
            ("django.forms.fields.DateTimeField", "DateTimeField"),
            ("django.forms.fields.DecimalField", "DecimalField"),
            ("django.forms.fields.EmailField", "EmailField"),
            ("django.forms.fields.FileField", "FileField"),
            ("django.forms.fields.FloatField", "FloatField"),
            (
                "django.forms.fields.GenericIPAddressField",
                "GenericIPAddressField"
            ),
            ("django.forms.fields.IntegerField", "IntegerField"),
            ("django.forms.fields.MultipleChoiceField", "MultipleChoiceField"),
            ("django.forms.fields.SlugField", "SlugField"),
            ("django.forms.fields.SplitDateTimeField", "SplitDateTimeField"),
            ("django.forms.fields.TimeField", "TimeField"),
            ("django.forms.fields.URLField", "URLField"),
            ("django.forms.fields.UUIDField", "UUIDField"),
            ("formfactory.fields.ParagraphField", "ParagraphField"),
    ],
    "widget-types": [
        ("django.forms.widgets.CheckboxInput", "CheckboxInput"),
        (
            "django.forms.widgets.CheckboxSelectMultiple",
            "CheckboxSelectMultiple"
        ),
        ("django.forms.widgets.DateInput", "DateInput"),
        ("django.forms.widgets.DateTimeInput", "DateTimeInput"),
        ("django.forms.widgets.EmailInput", "EmailInput"),
        ("django.forms.widgets.FileInput", "FileInput"),
        ("django.forms.widgets.HiddenInput", "HiddenInput"),
        ("django.forms.widgets.NullBooleanSelect", "NullBooleanSelect"),
        ("django.forms.widgets.NumberInput", "NumberInput"),
        ("django.forms.widgets.PasswordInput", "PasswordInput"),
        ("django.forms.widgets.RadioSelect", "RadioSelect"),
        ("django.forms.widgets.Select", "Select"),
        ("django.forms.widgets.SelectMultiple", "SelectMultiple"),
        ("django.forms.widgets.Textarea", "Textarea"),
        ("django.forms.widgets.TextInput", "TextInput"),
        ("django.forms.widgets.TimeInput", "TimeInput"),
        ("django.forms.widgets.URLInput", "URLInput"),
        ("formfactory.widgets.ParagraphWidget", "ParagraphWidget")
    ],
    "error-types": [
        "empty", "incomplete", "invalid", "invalid_choice", "invalid_image",
        "invalid_list", "invalid_date", "invalid_time", "invalid_pk_value",
        "list", "max_decimal_places", "max_digits", "max_length", "max_value",
        "max_whole_digits", "min_length", "min_value", "missing", "required",
    ],
    "redirect-url-param-name": "next",
})


_registry = {
    "actions": {},
    "validators": {},
    "clean_methods": {}
}
