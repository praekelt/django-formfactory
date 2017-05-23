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
            "{% render_form <form_slug> %}"
        )

    # We do allow for the full object to be passed on context.
    if isinstance(tokens[1], basestring):
        return RenderFormNode(slug=tokens[1])

    # TODO Stil lrequires testing.
    elif isinstance(token[1], models.Form):
        return RenderFormNode(form=tokens[1])


class RenderFormNode(template.Node):

    def __init__(self, slug=None, form=None):
        self.slug = slug
        self.form = form

    def render(self, context):
        if self.slug:
            try:
                form = models.Form.objects.get(slug=self.slug)
            except models.Form.DoesNotExist:
                raise Http404("No FormFactory Form matches the given query.")
        elif self.form:
            form = self.form
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
        result.render()
        html = result.rendered_content
        return html
