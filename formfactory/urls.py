from django.conf.urls import url

from formfactory.views import FactoryFormView


urlpatterns = [
    url(r"^(?P<slug>[-\w]+)/$", FactoryFormView.as_view(), name="form-detail")
]
