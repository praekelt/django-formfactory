from django.conf.urls import url

from formfactory.views import FactoryFormView, FactoryWizardView


urlpatterns = [
    url(
        r"^wizard/(?P<slug>[\w-]+)(?:/(?P<step>[\w-]+))?/$",
        FactoryWizardView.as_view(url_name="formfactory:wizard-detail"),
        name="wizard-detail"
    ),
    url(r"^(?P<slug>[-\w]+)/$", FactoryFormView.as_view(), name="form-detail"),
]
