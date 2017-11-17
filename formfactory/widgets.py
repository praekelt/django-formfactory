from django.forms.widgets import Widget

# TODO Add django 19 and 110 render support
class ParagraphWidget(Widget):
    template_name = "formfactory/forms/widgets/paragraph.html"
