from django.views import generic

from formfactory.models import Form


class FormDetailView(generic.detail.DetailView):
    model = Form
    template = "formfactory/form_detail.html"


class FormListView(generic.list.ListView):
    model = Form
    template = "formfactory/form_list.html"
