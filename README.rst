Django Form Factory
===================
**Dynamic django form builder.**

.. image:: https://travis-ci.org/praekelt/django-formfactory.svg?branch=develop
    :target: https://travis-ci.org/praekelt/django-formfactory

.. image:: https://coveralls.io/repos/github/praekelt/django-formfactory/badge.svg?branch=develop
    :target: https://coveralls.io/github/praekelt/django-formfactory?branch=develop

.. contents:: Contents
    :depth: 5

Installation
------------

#. Install or add ``django-formfactory`` to your Python path.

#. Add ``formfactory`` to your ``INSTALLED_APPS`` setting.

#. Add ``url(r'^formfactory/', include("formfactory.urls", namespace="formfactory"))`` to your ``url patterns`` (only required if you intend on using the detail view)

Dependencies
------------

FormFactory makes use of the python markdown package as well as djano-simplemde. The latest tested version are pinned within ``formfactory/tests/requirements/<django_version>.txt``

Usage
-----

``django-formfactory`` allows users to create forms and wizards in the CMS.

Settings
~~~~~~~~

FORMFACTORY["field-types"]
    Control the form fields types that can be selected in Admin.
    Supports adding non Django fields: ``("<module_for_field>", "<display_name>")``
    eg. ``("formfactory.fields.ParagraphField", "ParagraphField")``

FORMFACTORY["widget-types"]
    Control the form widget types that can be selected in Admin.
    Supports adding non Django widgets: ``("<module_for_widget>", "<display_name>")``
    eg. ``("formfactory.widgets.ParagraphWidget", "ParagraphWidget")``

Widgets and Fields
------------------
FormFactory ships with a ParagraphField and ParagraphWidget combo. The intended use for these is to allow copy to be added in between fields.
Allows for the same base templates to be used in most cases.

Views
~~~~~

``django-formfactory`` provide a base ``FormView`` and ``FactoryWizardView``
which can both be used directly or subclassed if you require extra context
or form data processing.

Templates
~~~~~~~~~

``django-formfactory`` allows you to either override the template for all forms
by adding a template ``formfactory/form_detail.html`` or an individual form by
adding a template ``formfactory/form_detail_<form-slug>.html`` to your project's
template dir. As well as ``formfactory/inclusion_tags/form_detail.html`` and
``formfactory/inclusion_tags/form_detail_<form-slug>.html`` for the inclusion
tags.

Inclusiontag
~~~~~~~~~~~~

Use the inclusion tag which has been provided:
``{% render_form form_object %}``


Models
~~~~~~

**FormData:**
    A basic store for user submitted form data.
        - uuid: a common uuid for each data item in the data set
        - form: the ``Form`` object

**FormDataItem:**
    A per field value store, encapsulated by a ``FormData`` object.
        - form_data: the ``FormData`` object
        - form_field: the ``FormField`` object
        - value: a text value of what was submitted for a particular field

**Action:**
    An action which will be triggered in order when the form is saved.
        - action: a choice of all registered actions in the project
        - as_function: a property which returns the action function

**ActionParam:**
    Params that are required by the predefined or custom action functions. Passed to the action as a set of kwargs.
        - key: param name
        - value: param value
        - action: the ``Action`` object

**Form:**
    A form object which encapsulates a set of form fields and defines the actions that will be performed on save.
        - title: a descriptive title
        - slug: url friendly identifier
        - actions: a set of ``Action`` objects to be performed in order on save
        - success_message: The message string that will be displayed by the django messages framework on successful submission of the form
        - failure_message: The message string that will be displayed by the django messages framework if a form submission fails
        - ajax_post: Flag that enables JS ajax posting on the default formfactory templates, or to be used as a hook when overriding templates.


**Wizard:**
    A wizard object that encapsulates a list of forms and actions that will be performed on the WizardView's ``done`` step.
        - title: a descriptive title
        - slug: url friendly identifier
        - forms: a set of ordered forms mapping to each step in the WizardView.
        - redirect_to: The URL which should should be redirect to after the wizard's done step (e.g. "/").
        - actions: a set of ordered ``Action`` objects to be performed in order in the WizardView's ``done`` step.
        - success_message: The message string that will be displayed by the django messages framework on successful submission of the form
        - failure_message: The message string that will be displayed by the django messages framework if a form submission fails

    Each form's ``save()`` method is called in the ``done`` step. This ensures that all actions defined for each form are
    performed. Following that, wizard actions are then performed before the WizardView redirects.

    The URL to which the WizardView redirects can be specified in one of two ways:
    - It can be specified in the CMS in the ``redirect_to`` field on the wizard object.
    - It can be specified as a GET query parameter on the URL. The query parameter key can be specified by setting
    ``FORMFACTORY["redirect-url-param-name"]`` in your settings file.

**FieldChoice:**
    A set of field choices that a populated into `MultiSelect` and `Select` widgets
        - label: human readable dropdown label
        - value: the value that will be submitted

**FormFieldGroup:**
    A model which encapsulates a set of form fields.
        - title: the title to be used in the formset legend when rendered
        - forms: the ``Forms`` this grouping is associated to

**FormField:**
    Defines a form field with all options and required attributes. Encapsulated by the ``Form`` object.
        - title: a descriptive title
        - slug: url friendly identifier
        - position: the position at which the field should be rendered in the form
        - form_groups: the ``FormFieldGroups`` this field is associated to
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

Model Choices
~~~~~~~~~~~~~

To define a custom model for field choices the model will need to have an items related name which points to an enum items model containing key and value fields. ::

    from django.db import models

    class Enum(models.Model):
        title = models.CharField(max_length=100)

    class EnumItem(models.Model):
        enum = models.ForeignKey(Enum, related_name="items")
        value = models.CharField(max_length=100)
        label = models.CharField(max_length=100)

Actions
~~~~~~~

FormFactory come with some predefined actions:
    - store_data: stores the submitted date to a key/value store_data. Requires no ``ActionParam``
    - send_email: sends the data via email. Requires the following ``ActionParam``
        - from_email_field: mapping to the form field that the email will be sent from
        - to_email_field: mapping to the form field that the email will be sent to
        - subject_field: mapping to the form field that will be used for the email subject
    - login: logs a user in. Requires the following ``ActionParam``
        - username_field: mapping to the form field where the username will be completed.
        - password_field: mapping to the form field where the username will be completed.
    - file_upload: handles uploading files to a predefined path. Requires the following ``ActionParam``
        - upload_path_field: mapping to the form field where the upload path has been set.

Custom actions can be added by creating a function in <yourapp or project>/formfactoryapp/actions.py. For example::

    from formfactory import actions

    @actions.register
    def my_custom_action(form_instance, **kwargs):
        # do some stuff

Validation
~~~~~~~~~~

Custom validators can be added by creating a function in <yourapp or project>/formfactoryapp/validators.py. For example::

    from formfactory import validators

    @validators.register
    def my_custom_validator(value):
        if not condition:
            raise ValidationError("Failed")
        return True

