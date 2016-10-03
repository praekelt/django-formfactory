from django import template


register = template.Library()


@register.inclusion_tag(
    "formfactory/inclusion_tags/form_detail.html", takes_context=True
)
def render_link(context, obj):
    context["object"] = obj
    return context
