from django.conf.urls import url

from formfactory.views import FormCreateView


urlpatterns = [
    url(r"^(?P<slug>[-\w]+)/$", FormCreateView.as_view(), name="form-detail")
]
