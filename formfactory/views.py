from django.views import generic

from formfactory.models import Form


class FormDetailView(generic.detail.DetailView):
    model = Form


class FormListView(generic.list.ListView):
    model = Form
