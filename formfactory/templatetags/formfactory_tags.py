from django import template

from formfactory.models import Form

register = template.Library()


@register.inclusion_tag(
    "formfactory/inclusion_tags/form_detail.html", takes_context=True
)
def render_form(context, obj):
    context["object"] = Form.objects.get_object_or_404(slug=obj)
    return context
