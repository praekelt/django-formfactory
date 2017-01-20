from django.contrib import admin

from formfactory import forms, models, utils


class FieldChoiceModelAdmin(admin.ModelAdmin):
    form = forms.FieldChoiceAdminForm
    model = models.FieldChoice


class FormActionParamInline(admin.StackedInline):
    form = forms.ActionParamAdminForm
    model = models.ActionParam


class ActionModelAdmin(admin.ModelAdmin):
    form = forms.ActionAdminForm
    model = models.Action
    inlines = [FormActionParamInline]


class FormFieldInline(admin.StackedInline):
    form = forms.FormFieldAdminForm
    model = models.FormField
    prepopulated_fields = {"slug": ["title"]}


class FormActionThroughInline(admin.StackedInline):
    form = forms.FormActionThroughAdminForm
    model = models.FormActionThrough


class FormAdmin(admin.ModelAdmin):
    form = forms.FormAdminForm
    list_display = ["title"]
    inlines = [FormFieldInline, FormActionThroughInline]
    prepopulated_fields = {"slug": ["title"]}


class FormDataItemInline(admin.StackedInline):
    form = forms.FormDataItemAdminForm
    model = models.FormDataItem
    readonly_fields = utils.get_all_model_fields(models.FormDataItem)


class FormDataAdmin(admin.ModelAdmin):
    form = forms.FormDataAdminForm
    model = models.FormData
    inlines = [FormDataItemInline]
    readonly_fields = ("form", "uuid")


admin.site.register(models.Action, ActionModelAdmin)
admin.site.register(models.FieldChoice, FieldChoiceModelAdmin)
admin.site.register(models.Form, FormAdmin)
admin.site.register(models.FormData, FormDataAdmin)
