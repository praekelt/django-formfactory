from django.contrib import admin

from formfactory import forms
from formfactory.models import FieldChoice, Form, FormField


class FieldChoiceModelAdmin(admin.ModelAdmin):
    form = forms.FieldChoiceAdminForm
    models = FieldChoice


class FormFieldInline(admin.StackedInline):
    form = forms.FormFieldAdminForm
    model = FormField


class FormAdmin(admin.ModelAdmin):
    form = forms.Form
    list_display = ["title"]
    inlines = [FormFieldInline]
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(FieldChoice, FieldChoiceModelAdmin)
admin.site.register(Form, FormAdmin)
