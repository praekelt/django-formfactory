from django.conf.urls import url

from formfactory.views import FormDetailView, FormListView


urlpatterns = [
    url(r"^$", FormListView.as_view(), name="form-list"),
    url(r"^(?P<slug>[-\w]+)/$", FormDetailView.as_view(), name="form-detail")
]
