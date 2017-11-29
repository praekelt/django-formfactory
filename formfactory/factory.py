from uuid import uuid4
import importlib
import inspect

from django import forms
from django.conf import settings
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from formfactory import SETTINGS, utils


class FormFactory(forms.Form):
    """Builds a form class from defined fields passed to it by the Form model.
    """
    uuid = forms.UUIDField(
        initial=unicode(uuid4()), widget=forms.HiddenInput
    )
    form_id = forms.CharField(
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        self.actions = kwargs.pop("actions")
        self.clean_method = kwargs.pop("clean_method")
        self.request = kwargs.pop("request", None)

        self.form_id = form_id = kwargs.pop("form_id")
        defined_field_groups = kwargs.pop("field_groups")

        super(FormFactory, self).__init__(*args, **kwargs)

        # Set initial value
        self.fields["form_id"].initial = form_id

        # Iterates over the fields defined in the Form model and sets the
        # appropriate attributes and builds up the fieldgroups.
        self.field_group = []

        # Models aren't ready when the file is initially processed.
        from formfactory import models
        field_through = models.FieldGroupThrough
        for field_group in defined_field_groups:

            fields = utils.order_by_through(
                field_group.fields.all(),
                "FieldGroupThrough",
                "field_group",
                field_group,
                "field"
            )
            self.field_group.append(
                [field_group.title, field_group.show_title, [f.slug for f in fields]]
            )
            for field in fields:
                field_meta = field.get_field_meta
                field_type = getattr(field_meta[0], field_meta[1])

                additional_validators = []
                for validator in field.additional_validators.all():
                    additional_validators.append(
                        validator.as_function
                    )

                # NOTE: Label always defaults to title if label field is empty,
                # this is not expected behaviour. Label needs to be optional.
                field_args = {}

                # Some custom fields might need extra info passed to the actual
                # field instance. Only cater for leaf args.
                init_args = inspect.getargspec(field_type.__init__).args
                for arg in init_args:
                    field_value = getattr(field, arg, None)
                    if field_value:
                        field_args[arg] = field_value

                # Ensure the expected values are always present on a specific
                # default subset.
                field_args.update({
                    "label": field.label,
                    "initial": field.initial or self.initial.get(field.slug),
                    "required": field.required,
                    "disabled": field.disabled,
                    "help_text": field.help_text,
                    "validators": additional_validators,
                    "error_messages": dict(
                        (m.key, m.value) for m in field.error_messages.all()
                    )
                })

                # Sets the user defined widget if setup
                if field.widget:
                    widget_meta = field.get_widget_meta
                    widget = getattr(widget_meta[0], widget_meta[1])
                    field_args["widget"] = widget()

                self.fields[field.slug] = field_type(**field_args)

                # Saves the field model pk to the form field to prevent the
                # need for another query in the save method.
                self.fields[field.slug].field_pk = field.pk

                # Adds the field choices and max_length but catches the
                # exception as not all fields allow for these attrs.
                choices = None
                if field.choices.exists():
                    choices = tuple(
                        (c.value, c.label) for c in field.choices.all()
                    )
                    try:
                        self.fields[field.slug].choices = choices
                    except TypeError:
                        pass

                if field.model_choices and \
                        hasattr(field.model_choices, "items") and \
                        field.model_choices.items.exists():
                    choices = tuple(
                        (c.value, c.label)
                        for c in field.model_choices.items.all()
                    )
                    try:
                        if self.fields[field.slug].choices:
                            self.fields[field.slug].choices += choices
                        else:
                            self.fields[field.slug].choices = choices
                    except TypeError:
                        pass

                try:
                    if field.max_length:
                        self.fields[field.slug].max_length = field.max_length
                except TypeError:
                    pass

                # Adds widget-specific options to the form field
                # TODO add pluggable attrs, can be assigned for now other
                # fields on the form model. probably use widget class and settings.
                # TODO Allowed attrs (widget_attrs["paragraph"] = field.paragraph)
                widget_attrs = self.fields[field.slug].widget.attrs
                if field.placeholder is not None:
                    widget_attrs["placeholder"] = field.placeholder
                if choices:
                    self.fields[field.slug].widget.choices = choices

    def _html_output(self, normal_row, error_row, row_ender, help_text_html,
                     errors_on_separate_row):
        """Helper function for outputting HTML. Used by as_table(), as_ul(),
        as_p(). Copied directly from django.forms.BaseForm._html_output and
        modified to deal with field groups.
        """
        # Errors that should be displayed above all fields.
        top_errors = self.non_field_errors()
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ""
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_("(Hidden field %(name)s) %(error)s") % {"name": name, "error": force_text(e)}
                         for e in bf_errors])
                hidden_fields.append(six.text_type(bf))

        for fieldset_label, show_title, fieldnames in self.field_group:
            snippet = """<fieldset class="Fieldset">"""
            if show_title:
                snippet += "<legend Fieldsetlegend>%s</legend>" % fieldset_label
            output.append(snippet)

            for name in fieldnames:
                field = self.fields[name]

                html_class_attr = ""
                bf = self[name]

                # Escape and cache in local variable.
                bf_errors = self.error_class(
                    [conditional_escape(error) for error in bf.errors]
                )
                if not bf.is_hidden:
                    # Create a 'class="..."' atribute if the row should have
                    # any CSS classes applied.
                    css_classes = bf.css_classes()
                    if css_classes:
                        html_class_attr = " class=\"%s\"" % css_classes

                    if errors_on_separate_row and bf_errors:
                        output.append(error_row % force_text(bf_errors))

                    if bf.label:
                        label = conditional_escape(force_text(bf.label))
                        label = bf.label_tag(label) or ""
                    else:
                        label = ""

                    if field.help_text:
                        help_text = help_text_html % force_text(
                            field.help_text
                        )
                    else:
                        help_text = ""

                    output.append(normal_row % {
                        "errors": force_text(bf_errors),
                        "label": force_text(label),
                        "field": six.text_type(bf),
                        "help_text": help_text,
                        "html_class_attr": html_class_attr,
                        "field_id": "id_%s" % name
                    })

            output.append("</fieldset>")

        if top_errors:
            output.insert(0, error_row % force_text(top_errors))

        # Insert any hidden fields in the last row.
        if hidden_fields:
            # Add the hidden fields outside of the fieldset grouping.
            str_hidden = "".join(hidden_fields)
            output.append(str_hidden)
        return mark_safe("\n".join(output))

    def clean(self, **kwargs):
        """Performs form level cleaning of field data.
        """
        kwargs.update({"request": self.request})
        clean_method = self.clean_method
        if clean_method:
            clean_method.as_function(form_instance=self, **kwargs)
        return self.cleaned_data

    def save(self, *args, **kwargs):
        """Performs the required actions in the defined sequence.
        """

        # Models aren't ready when the file is initially processed.
        from formfactory import models
        form = models.Form.objects.get(id=self.form_id)
        actions = utils.order_by_through(
            self.actions,
            "FormActionThrough",
            "form",
            form,
            "action"
        )
        for action in actions:
            action_params = kwargs.copy()
            action_params.update(dict(
                (obj.key, obj.value) for obj in action.params.all()
            ))
            action.as_function(form_instance=self, **action_params)
