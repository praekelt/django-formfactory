from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(
        r"^formfactory/", include("formfactory.urls", namespace="formfactory")
    ),
    url(
        r"^render_tag/$",
        TemplateView.as_view(template_name="tests/render_tag.html"),
        name="render_tag"
    ),
    url(
        r"^render_tag_all_fields/$",
        TemplateView.as_view(template_name="tests/render_tag_all.html"),
        name="render_tag_all_fields"
    ),
    url(
        r"^render_tag_404/$",
        TemplateView.as_view(template_name="tests/render_tag_404.html"),
        name="render_tag_404"
    ),
    url(
        r"^render_tag_syntax_error/$",
        TemplateView.as_view(template_name="tests/render_tag_syntax_error.html"),
        name="render_tag_syntax_error"
    ),
]
