from django import template
from django.http import Http404

from formfactory import models

register = template.Library()


@register.inclusion_tag(
    "formfactory/inclusion_tags/form_detail.html", takes_context=True
)
def render_form(context, object_or_slug):
    render_dict = dict()
    if isinstance(object_or_slug, models.Form):
        render_dict["object"] = object_or_slug
    elif isinstance(object_or_slug, basestring):
        try:
            render_dict["object"] = models.Form.objects.get(slug=object_or_slug)
        except models.Form.DoesNotExist:
            raise Http404("No FormFactory Form matches the given query.")
    return render_dict
