from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import generic

from formtools.wizard.views import NamedUrlSessionWizardView

from formfactory import SETTINGS
from formfactory.forms import EmptyForm
from formfactory.models import Form, Wizard


class FactoryFormView(generic.FormView):
    template_name = "formfactory/form_detail.html"
    form_slug = None
    redirect_to = None

    def __init__(self, *args, **kwargs):
        super(FactoryFormView, self).__init__(*args, **kwargs)
        self.form_object = None

    def form_valid(self, form):
        form.save(request=self.request)
        messages.add_message(
            self.request, messages.SUCCESS, self.form_object.success_message
        )
        return super(FactoryFormView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR, self.form_object.failure_message
        )
        return super(FactoryFormView, self).form_invalid(form)

    def get_form(self, form_class=None):
        self.form_object = get_object_or_404(
            Form, slug=self.kwargs.get("slug", self.form_slug)
        )
        if self.request.POST or self.request.FILES:
            return self.form_object.as_form(
                self.request.POST, self.request.FILES
            )
        return self.form_object.as_form()

    def get_success_url(self):
        redirect_url = self.request.GET.get(
            SETTINGS["redirect-url-param-name"]
        ) or self.redirect_to
        if redirect_url:
            return redirect_url
        return self.request.path_info


class FactoryWizardView(NamedUrlSessionWizardView):
    form_list = [EmptyForm, ]

    def dispatch(self, request, *args, **kwargs):
        # TODO Read config from DB
        wizard_slug = kwargs.get("slug")
        wizard = Wizard.objects.get(slug=wizard_slug)
        form_list = wizard.forms.all()
        forms = ()
        for form in form_list:
            forms += (form.slug, form.as_form)
        # We need to re-initialise the form kwargs for this particular
        # request.
        # TODO: We may have to add context_dict, etc.
        init_kwargs = self.get_initkwargs(form_list=forms, url_name="wizard")
        self.form_list = init_kwargs["form_list"]
        # self.form_kwargs = config["form_kwargs"]
        # self.context_dict = config["context_dict"]
        return super(FactoryWizardView, self).dispatch(request, *args, **kwargs)

    def get_form(self, step=None, data=None, files=None):
        """We need to override this method so that we can create
        form instances from formfactory on-the-fly. """
        # cherry-picking some stuff from parents
        if step is None:
            step = self.steps.current
        kwargs = self.get_form_kwargs(step)
        kwargs.update({
            "data": data,
            "files": files,
        })
        obj = self.form_list["step"]
        return obj.as_form(**kwargs)

    def done(self, form_list, **kwargs):
        import pdb;pdb.set_trace()