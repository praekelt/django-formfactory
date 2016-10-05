Django Form Factory
===================
**Dynamic django form builder.**

.. figure:: https://travis-ci.org/praekelt/django-formfactory.svg?branch=develop
   :align: center
   :alt: Travis

.. contents:: Contents
    :depth: 5

Installation
------------

#. Install or add ``django-formfactory`` to your Python path.

#. Add ``formfactory`` to your ``INSTALLED_APPS`` setting.

#. Add ``url(r'^formfactory/', include("formfactory.urls", namespace="formfactory"))`` to your ``url patterns`` (only required if you intend on using the detail view)

Usage
-----

Settings
~~~~~~~~

#. FORMFACTORY["field-types"]: Control the form fields types that can be selected in Admin.

#. FORMFACTORY["email-action"]["email-action"]: Control the form fields types that can be selected in Admin.

Views
~~~~~

``django-formfactory`` provide a base ``FormView`` which can be used directly or
subclassed if you require extra context or form data processing.

Inclusiontag
~~~~~~~~~~~~

Use the inclusion tag which has been provided:
``{% render_form form_object %}``

Models
~~~~~~

...
