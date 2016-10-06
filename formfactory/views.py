from django.views import generic
from django.shortcuts import get_object_or_404

from formfactory.models import Form


class FormCreateView(generic.FormView):
    template_name = "formfactory/form_detail.html"

    def form_valid(self, form):
        form.save()
        return super(FormCreateView, self).form_valid(form)

    def get_form(self, form_class=None):
        form_obj = get_object_or_404(Form, slug=self.kwargs.get("slug"))
        return form_obj.as_form(self.request.POST)

    def get_success_url(self):
        return self.request.META.get(
            "HTTP_REFERER", self.request.META.get("PATH_INFO")
        )
