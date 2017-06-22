from django import template
from django.core.urlresolvers import reverse, resolve
from django.http import Http404

from formfactory import models

register = template.Library()


@register.tag()
def render_form(parser, token):
    """{% render_form <form_slug> %}"""
    tokens = token.split_contents()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError(
            "{% render_form <form_slug>/<object> %}"
        )

    return RenderFormNode(variable=tokens[1])


class RenderFormNode(template.Node):

    def __init__(self, variable):
        self.variable = template.Variable(variable)

    def render(self, context):
        try:
            variable = self.variable.resolve(context)
        except template.VariableDoesNotExist:
            variable = self.variable.var
        default_msg = "No FormFactory Form matches the given query. %s" % self.variable

        # If the variable is a string type we attempt to find object based on
        # slug field, otherwise we pass the object along directly.
        if isinstance(variable, basestring):
            try:
                form = models.Form.objects.get(slug=variable)
            except models.Form.DoesNotExist:
                raise Http404(default_msg)
        elif isinstance(variable, models.Form):
            form = variable
        else:
            raise Http404(default_msg)

        url = form.absolute_url
        view, args, kwargs = resolve(url)
        request = context["request"]

        # Store original request values.
        original_method = request.method
        original_path = request.path
        original_info = request.path_info

        # Assign new request values.
        request.method = "GET"
        request.path = url
        request.path_info = url

        # Call view to get result.
        kwargs["inclusion_tag"] = True
        result = view(request, *args, **kwargs)

        # Replace request values with originals.
        request.method = original_method
        request.path = original_path
        request.path_info = original_path

        # We don't expect anything other than a TemplateResponse here.

        # Explicitly set the form context to be the incoming context, current
        # request context should always override clean context data from
        # instantiating the view. Only to be replaced if the context object
        # matches the one the view provides.
        if result.context_data["object"] == context.get("object", None):
            for key, value in result.context_data.items():
                if context.get(key, None):
                    result.context_data[key] = context[key]
        result.render()
        html = result.rendered_content
        return html
