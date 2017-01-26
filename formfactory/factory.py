from uuid import uuid4

from django import forms
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils import six
from django.utils.translation import ugettext_lazy as _


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

        form_id = kwargs.pop("form_id")
        defined_field_groups = kwargs.pop("field_groups")

        super(FormFactory, self).__init__(*args, **kwargs)

        # Set initial value
        self.fields["form_id"].initial = form_id

        # Iterates over the fields defined in the Form model and sets the
        # appropriate attributes and builds up the fieldgroups.
        self.field_group = []
        for field_group in defined_field_groups:
            fields = field_group.fields.all().order_by("fieldgroupthrough")
            self.field_group.append(
                [field_group.title, field_group.show_title, [f.slug for f in fields]]
            )
            for field in fields:
                field_type = getattr(forms, field.field_type)

                additional_validators = []
                if field.additional_validators:
                    additional_validators = [field.additional_validators]

                self.fields[field.slug] = field_type(
                    label=field.label,
                    initial=field.initial,
                    required=field.required,
                    disabled=field.disabled,
                    help_text=field.help_text,
                    validators=additional_validators
                )

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

                try:
                    if field.max_length:
                        self.fields[field.slug].max_length = field.max_length
                except TypeError:
                    pass

                # Sets the user defined widget if setup
                if field.widget:
                    widget = getattr(forms.widgets, field.widget)
                    self.fields[field.slug].widget = widget()

                # Adds widget-specific options to the form field
                widget_attrs = self.fields[field.slug].widget.attrs
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
            html_class_attr = ''
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': force_text(e)}
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
                field.widget.attrs["placeholder"] = field.initial or \
                    field.label
                bf = self[name]

                if not bf.is_hidden:
                    # Create a 'class="..."' atribute if the row should have
                    # any CSS classes applied.
                    css_classes = bf.css_classes()
                    if css_classes:
                        html_class_attr = " class=\"%s\"" % css_classes

                    if errors_on_separate_row and bf_errors:
                        output.append(error_row % force_text(bf_errors))

                    if bf.label:
                        label = ""
                        if field.required:
                            label = "* "
                        label += conditional_escape(force_text(bf.label))
                    else:
                        label = ''

                    if field.help_text:
                        help_text = help_text_html % force_text(
                            field.help_text
                        )
                    else:
                        help_text = ''

                    output.append(normal_row % {
                        "errors": force_text(bf_errors),
                        "label": force_text(label),
                        "field": six.text_type(bf),
                        "help_text": help_text,
                        "html_class_attr": html_class_attr,
                        "field_id": "id_%s" % name
                    })

                # Escape and cache in local variable.
                bf_errors = self.error_class(
                    [conditional_escape(error) for error in bf.errors]
                )

            output.append("</fieldset>")

        if top_errors:
            output.insert(0, error_row % force_text(top_errors))

        # Insert any hidden fields in the last row.
        if hidden_fields:
            str_hidden = "".join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {
                        "errors": "", "label": "",
                        "field": "", "help_text": "",
                        "html_class_attr": html_class_attr,
                        "field_id": ""
                    })
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + \
                    row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe("\n".join(output))

    def save(self, *args, **kwargs):
        """Performs the required actions in the defined sequence.
        """
        for action in self.actions.order_by("formactionthrough"):
            action_params = kwargs.copy()
            action_params.update(dict(
                (obj.key, obj.value) for obj in action.params.all()
            ))
            action.as_function(form_instance=self, **action_params)
