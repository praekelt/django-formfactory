============
Form builder
============

Overview
========
The form builder allows you to create forms in the CMS. The is achieved by abstracting
form fields and the actual forms as models. A user can create form fields, choose the
order in which they should be rendered on the form, and can group them.

Overriding templates
====================

Models
======

**Form:**
    A form object which encapsulates a set of form fields and defines the actions that will be performed on save.
        - title: a descriptive title
        - slug: url friendly identifier
        - actions: a set of ``Action`` objects to be performed in order on save
        - success_message: The message string that will be displayed by the django messages framework on successful submission of the form
        - failure_message: The message string that will be displayed by the django messages framework if a form submission fails

**FormField:**
    Defines a form field with all options and required attributes. Encapsulated by the ``Form`` object.
        - title: a descriptive title
        - slug: url friendly identifier
        - position: the position at which the field should be rendered in the form
        - form_groups: the ``FormFieldGroup``s this field is associated to
        - field_type: a set of field type, defined in the app settings
        - widget: a set of widgets, defined in app settings
        - label: the field label text
        - initial: an initial value the field will be populated with
        - max_length: the maximum length a value can be
        - help_text: a helpful string that will be rendered below the field
        - placeholder: a string that will be rendered as the field placeholder
        - required: boolean value to indicate if the field is required
        - disabled: boolean value to disable field (readonly)
        - choices: a set of ``FieldChoice`` objects
        - model_choices: a generic foreign key to a model which defines the choices for the formfield
        - additional_validators: a set of custom defined field validators

**FormFieldGroup:**
    A model which encapsulates a set of form fields.
        - title: the title to be used in the formset legend when rendered
        - forms: the ``Form``s this grouping is associated to



Actions
=======

Custom form field validators
============================
Custom validators can be added by creating a function in <yourapp or project>/formfactoryapp/validators.py. For example::

    # {{ your app }}/formfactoryapp/validators.py
    from formfactory import validators

    @validators.register
    def my_custom_validator(value):
        if not condition:
            raise ValidationError("Failed")
        return True

