from django.conf import settings


# TODO add contenttype settings in
class AppFields(object):
    DJANGO = "django.forms.fields"
    FORMFACTORY = "formfactory.fields"

class AppWidgets(object):
    DJANGO = "django.forms.widgets"
    FORMFACTORY = "formfactory.widgets"

SETTINGS = getattr(settings, "FORMFACTORY", {
    "field-types": [
            ("%s.BooleanField" % AppFields.DJANGO, "BooleanField"),
            ("%s.CharField" % AppFields.DJANGO, "CharField"),
            ("%s.ChoiceField" % AppFields.DJANGO, "ChoiceField"),
            ("%s.DateField" % AppFields.DJANGO, "DateField"),
            ("%s.DateTimeField" % AppFields.DJANGO, "DateTimeField"),
            ("%s.DecimalField" % AppFields.DJANGO, "DecimalField"),
            ("%s.EmailField" % AppFields.DJANGO, "EmailField"),
            ("%s.FileField" % AppFields.DJANGO, "FileField"),
            ("%s.FloatField" % AppFields.DJANGO, "FloatField"),
            ("%s.GenericIPAddressField" % AppFields.DJANGO, "GenericIPAddressField"),
            ("%s.IntegerField" % AppFields.DJANGO, "IntegerField"),
            ("%s.MultipleChoiceField" % AppFields.DJANGO, "MultipleChoiceField"),
            ("%s.SlugField" % AppFields.DJANGO, "SlugField"),
            ("%s.SplitDateTimeField" % AppFields.DJANGO, "SplitDateTimeField"),
            ("%s.TimeField" % AppFields.DJANGO, "TimeField"),
            ("%s.URLField" % AppFields.DJANGO, "URLField"),
            ("%s.UUIDField" % AppFields.DJANGO, "UUIDField"),
            ("%s.ParagraphField" % AppFields.FORMFACTORY, "ParagraphField"),
    ],
    "widget-types": [
        ("%s.CheckboxInput" % AppWidgets.DJANGO, "CheckboxInput"),
        (
            "%s.CheckboxSelectMultiple" % AppWidgets.DJANGO,
            "CheckboxSelectMultiple"
        ),
        ("%s.DateInput" % AppWidgets.DJANGO, "DateInput"),
        ("%s.DateTimeInput" % AppWidgets.DJANGO, "DateTimeInput"),
        ("%s.EmailInput" % AppWidgets.DJANGO, "EmailInput"),
        ("%s.FileInput" % AppWidgets.DJANGO, "FileInput"),
        ("%s.HiddenInput" % AppWidgets.DJANGO, "HiddenInput"),
        ("%s.NullBooleanSelect" % AppWidgets.DJANGO, "NullBooleanSelect"),
        ("%s.NumberInput" % AppWidgets.DJANGO, "NumberInput"),
        ("%s.PasswordInput" % AppWidgets.DJANGO, "PasswordInput"),
        ("%s.RadioSelect" % AppWidgets.DJANGO, "RadioSelect"),
        ("%s.Select" % AppWidgets.DJANGO, "Select"),
        ("%s.SelectMultiple" % AppWidgets.DJANGO, "SelectMultiple"),
        ("%s.Textarea" % AppWidgets.DJANGO, "Textarea"),
        ("%s.TextInput" % AppWidgets.DJANGO, "TextInput"),
        ("%s.TimeInput" % AppWidgets.DJANGO, "TimeInput"),
        ("%s.URLInput" % AppWidgets.DJANGO, "URLInput"),
        ("%s.ParagraphWidget" % AppWidgets.FORMFACTORY, "ParagraphWidget")
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
