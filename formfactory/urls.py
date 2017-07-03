from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from formfactory.views import FactoryFormView, FactoryFormNoCSRFView, \
    FactoryWizardView


urlpatterns = [
    url(
        r"^wizard/(?P<slug>[\w-]+)(?:/(?P<step>[\w-]+))?/$",
        FactoryWizardView.as_view(url_name="formfactory:wizard-detail"),
        name="wizard-detail"
    ),
    url(
        r"^(?P<slug>[-\w]+)(?:/(?P<template_suffix>[\w-]+))?/$",
        FactoryFormView.as_view(),
        name="form-detail"
    ),
    url(
        r"^nocsrf/(?P<slug>[-\w]+)(?:/(?P<template_suffix>[\w-]+))?/$",
        csrf_exempt(FactoryFormNoCSRFView.as_view()),
        name="form-detail-nocsrf"
    )
]
