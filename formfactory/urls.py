from django.conf.urls import url

from formfactory.views import FactoryFormView, FactoryWizardView


urlpatterns = [
    url(r"^(?P<slug>[-\w]+)/$", FactoryFormView.as_view(), name="form-detail"),
    url(
        r"^(?P<slug>[\w-]+)(?:/(?P<step>[\w-]+))?/$",
        FactoryWizardView.as_view(url_name="formfactory:wizard"),
        name="wizard-detail"
    )
]
