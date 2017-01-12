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

    def get_prefix(self, request, *args, **kwargs):
        return "%s-%s" % (self.__class__.__name__, kwargs["slug"])

    def dispatch(self, request, *args, **kwargs):
        # TODO Read config from DB
        wizard_slug = kwargs.get("slug")
        wizard = Wizard.objects.get(slug=wizard_slug)
        # import pdb;pdb.set_trace()
        form_list = []
        self.form_list_map = {}
        for obj in wizard.forms.all():
            klass = obj.as_form().__class__
            form_list.append((obj.slug, klass))
            self.form_list_map[obj.slug] = obj
        # form_list = [obj.as_form().__class__ for obj in wizard.forms.all()]
        # forms = tuple((form.slug, form) for form in form_list)
        # We need to re-initialise the form kwargs for this particular
        # request.
        # TODO: We may have to add context_dict, etc.
        init_kwargs = self.get_initkwargs(form_list=form_list, url_name="formfactory:wizard")
        self.form_list = init_kwargs["form_list"]
        # self.form_kwargs = config["form_kwargs"]
        # self.context_dict = config["context_dict"]
        result = super(FactoryWizardView, self).dispatch(request, *args, **kwargs)
        return result

    def get_form(self, step=None, data=None, files=None):
        """We need to override this method so that we can create
        form instances from formfactory on-the-fly. """
        # cherry-picking some stuff from parents

        from django import forms

        if step is None:
            step = self.steps.current
        form_class = self.form_list[step]
        # prepare the kwargs for the form instance.
        kwargs = self.get_form_kwargs(step)
        kwargs.update({
            'data': data,
            'files': files,
        })
        if issubclass(form_class, (forms.ModelForm,
                                   forms.models.BaseInlineFormSet)):
            # If the form is based on ModelForm or InlineFormSet,
            # add instance if available and not previously set.
            kwargs.setdefault('instance', self.get_form_instance(step))
        elif issubclass(form_class, forms.models.BaseModelFormSet):
            # If the form is based on ModelFormSet, add queryset if available
            # and not previous set.
            kwargs.setdefault('queryset', self.get_form_instance(step))


        #import pdb;pdb.set_trace()
        #result = super(FactoryWizardView, self).get_form(step, data, files)
        obj = self.form_list_map[step]
        return obj.as_form(**kwargs)

    def get_step_url(self, step):
        from django.core.urlresolvers import reverse
        return reverse(self.url_name, kwargs={'step': step,
                                              "slug": "profile"})

    def done(self, form_list, **kwargs):
        #import pdb;pdb.set_trace()
        from django.http import HttpResponse
        self.storage.reset()
        return HttpResponse("done")
