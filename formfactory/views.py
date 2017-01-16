from django import forms
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
    redirect_to = None

    def get_prefix(self, request, *args, **kwargs):
        return "%s-%s" % (self.__class__.__name__, kwargs["slug"])

    def dispatch(self, request, *args, **kwargs):
        wizard_slug = kwargs.get("slug")
        self.wizard_object = Wizard.objects.get(slug=wizard_slug)
        form_list = []
        self.form_list_map = {}
        for obj in self.wizard_object.forms.all():
            klass = obj.as_form().__class__
            form_list.append((obj.slug, klass))
            self.form_list_map[obj.slug] = obj

        # We need to re-initialise the form kwargs for this particular
        # request. This allows for the next form_list to be added.
        init_kwargs = self.get_initkwargs(form_list=form_list, url_name=self.url_name)
        self.form_list = init_kwargs["form_list"]
        result = super(FactoryWizardView, self).dispatch(request, *args, **kwargs)
        return result

    def get_form(self, step=None, data=None, files=None):
        """We need to override this method so that we can create
        form instances from formfactory on-the-fly. """
        if step is None:
            step = self.steps.current
        form_class = self.form_list[step]

        # prepare the kwargs for the form instance.
        kwargs = self.get_form_kwargs(step)
        kwargs.update({
            "data": data,
            "files": files,
        })
        if issubclass(form_class, (forms.ModelForm,
                                   forms.models.BaseInlineFormSet)):
            # If the form is based on ModelForm or InlineFormSet,
            # add instance if available and not previously set.
            kwargs.setdefault("instance", self.get_form_instance(step))
        elif issubclass(form_class, forms.models.BaseModelFormSet):
            # If the form is based on ModelFormSet, add queryset if available
            # and not previous set.
            kwargs.setdefault("queryset", self.get_form_instance(step))

        obj = self.form_list_map[step]
        return obj.as_form(**kwargs)

    def get_step_url(self, step):
        from django.core.urlresolvers import reverse
        return reverse(self.url_name, kwargs={'step': step,
                                              "slug": "profile"})

    def done(self, form_list, form_dict, **kwargs):
        # run through all the wizard actions
        for action in self.wizard_object.as_wizard["actions"]:
            action_params = kwargs.copy()
            action_params.update(dict(
                (obj.key, obj.value) for obj in action.params.all()
            ))
            action.as_function(form_instance=self, **action_params)

        # TODO: provide a way a specify a redirect URL.
        from django.http import HttpResponse
        self.storage.reset()
        return HttpResponse("done")

    def get(self, *args, **kwargs):
        step_name = kwargs.get("step", None)

        # TODO: Hook a redirect that was specified
        if step_name is None:
            self.storage.extra_data["next"] = self.request.GET.get("next")
        return super(FactoryWizardView, self).get(*args, **kwargs)
