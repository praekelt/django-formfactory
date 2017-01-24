from django import template

from formfactory.models import Form


register = template.Library()


@register.inclusion_tag(
    "formfactory/inclusion_tags/form_detail.html", takes_context=True
)
def render_form(context, object_or_slug):
    context["object"] = Form.objects.get(slug=object_or_slug)
    return context
