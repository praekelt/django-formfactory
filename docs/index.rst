.. django-formfactory documentation master file, created by
   sphinx-quickstart on Wed Mar  1 16:28:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-formfactory's documentation!
==============================================

``django-formfactory`` is a CMS-driven form and wizard builder.

.. toctree::

    form
    wizard

Installation
============
#. Install or add ``django-formfactory`` to your python path, e.g.::

    pip install django-formfactory

#. Add ``"formfactory"`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        # ...
        "formfactory",
    ]

#. Add ``url(r"^formfactory/", include("formfactory.urls", namespace="formfactory"))`` to your urlpatterns.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
