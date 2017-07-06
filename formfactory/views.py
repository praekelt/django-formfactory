from django import forms
from django.core.urlresolvers import reverse
from django.core.files.storage import DefaultStorage
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic

from formtools.wizard.views import NamedUrlSessionWizardView

from formfactory import SETTINGS
from formfactory.models import Form, Wizard


class FactoryFormView(generic.FormView):
    form_slug = None
    redirect_to = None

    def __init__(self, *args, **kwargs):
        super(FactoryFormView, self).__init__(*args, **kwargs)
        self.form_object = None

    def get_template_names(self):
        template_names = []
        if self.template_name is not None:
            template_names = [self.template_name]
        template_names += [
            "formfactory/form_detail_%s.html" % self.form_object.slug,
            "formfactory/form_detail.html"
        ]
        return template_names

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
        return self.form_object.as_form(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(FactoryFormView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_prefix(self):
        return self.kwargs.get("slug", self.form_slug)

    def get_success_url(self):
        redirect_url = self.form_object.redirect_to or self.request.GET.get(
            SETTINGS["redirect-url-param-name"]) or self.redirect_to
        if redirect_url:
            return redirect_url
        return self.request.path_info

    def get_context_data(self, **kwargs):
        context = super(FactoryFormView, self).get_context_data(**kwargs)
        context.update({
            "form_object": self.form_object
        })
        return context


class FactoryFormNoCSRFView(FactoryFormView):
    """csrf_exempt is applied at class level independent of request so a full
    class is required for forms that are not subject to CSRF protection."""

    pass


class FactoryWizardView(NamedUrlSessionWizardView):
    form_list = [forms.Form]
    redirect_to = None
    file_storage = DefaultStorage()

    def get_prefix(self, request, *args, **kwargs):
        return "%s-%s" % (self.__class__.__name__, kwargs["slug"])

    def dispatch(self, request, *args, **kwargs):
        """
        This method is overridden to allow for the creation of `form_list`
        from the list of forms associated with this wizard instance
        """
        wizard_slug = kwargs.get("slug")
        self.wizard_object = Wizard.objects.get(slug=wizard_slug)
        self.form_list_map = {}
        self.form_object_list = self.wizard_object.forms.all().order_by(
            "wizardformthrough"
        )

        form_list = []
        for obj in self.form_object_list:
            klass = obj.as_form().__class__
            form_list.append((obj.slug, klass))
            self.form_list_map[obj.slug] = obj

        # We need to re-initialise the form kwargs for this particular
        # request. This allows for the next form_list to be added.
        init_kwargs = self.get_initkwargs(
            form_list=form_list, url_name=self.url_name
        )
        self.form_list = init_kwargs["form_list"]
        result = super(FactoryWizardView, self).dispatch(
            request, *args, **kwargs
        )
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
            "request": self.request
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
        return reverse(
            self.url_name, kwargs={
                "step": step, "slug": self.wizard_object.slug
            }
        )

    def done(self, form_list, form_dict, **kwargs):
        """ Save each form and run through all the wizard actions
        """
        for key, form in form_dict.items():
            form.save()

        for action in self.wizard_object.actions.all():
            action_params = kwargs.copy()
            action_params.update(dict(
                (obj.key, obj.value) for obj in action.params.all()
            ))
            action.as_function(form_dict=form_dict, **action_params)

        return HttpResponseRedirect(self.get_success_url())

    def get(self, *args, **kwargs):
        step_name = kwargs.get("step", None)
        redirect_name = SETTINGS["redirect-url-param-name"]
        if step_name is None:
            self.storage.extra_data[redirect_name] = \
                self.request.GET.get(redirect_name)
        return super(FactoryWizardView, self).get(*args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(FactoryWizardView, self).get_context_data(
            form, **kwargs)
        context["form_object"] = self.form_list_map[self.steps.current]
        context["form_object_list"] = self.form_object_list
        context["wizard_object"] = self.wizard_object
        return context

    def get_template_names(self):
        return [
            "formfactory/wizard_%s_step.html" % self.steps.current,
            "formfactory/wizard_detail_%s.html" % self.wizard_object.slug,
            "formfactory/wizard_detail.html"
        ]

    def get_success_url(self):
        stored_redirect = self.storage.extra_data.get(
            SETTINGS["redirect-url-param-name"]
        )
        redirect_url = self.wizard_object.redirect_to or \
            stored_redirect or self.redirect_to
        if redirect_url:
            return redirect_url
        return self.request.path_info
