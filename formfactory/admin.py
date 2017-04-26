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


class ValidatorModelAdmin(admin.ModelAdmin):
    form = forms.ValidatorAdminForm
    model = models.Validator


class CleanMethodModelAdmin(admin.ModelAdmin):
    form = forms.CleanMethodAdminForm
    model = models.CleanMethod


class FieldCustomErrorInline(admin.StackedInline):
    model = models.FormFieldErrorMessageProxy
    verbose_name = "Error message"
    verbose_name_plural = "Error messages"
    form = forms.CustomErrorInlineAdminForm


class FieldValidatorInline(admin.StackedInline):
    model = models.FormFieldValidatorProxy
    verbose_name = "Additional validator"
    verbose_name_plural = "Additional validators"


class CustomErrorModelAdmin(admin.ModelAdmin):
    form = forms.CustomErrorAdminForm
    model = models.CustomErrorMessage


class FormActionThroughInline(admin.StackedInline):
    form = forms.FormActionThroughAdminForm
    model = models.FormActionThrough


class FieldGroupFormThroughInline(admin.StackedInline):
    form = forms.FieldGroupFormThroughAdminForm
    model = models.FieldGroupFormThrough


class FormAdmin(admin.ModelAdmin):
    form = forms.FormAdminForm
    list_display = ["title"]
    inlines = [FieldGroupFormThroughInline, FormActionThroughInline]
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


class WizardFormThroughInline(admin.StackedInline):
    form = forms.WizardFormThroughAdminForm
    model = models.WizardFormThrough


class WizardActionThroughInline(admin.StackedInline):
    form = forms.WizardActionThroughAdminForm
    model = models.WizardActionThrough


class WizardAdmin(admin.ModelAdmin):
    form = forms.WizardAdminForm
    model = models.Wizard
    inlines = [WizardFormThroughInline, WizardActionThroughInline]
    prepopulated_fields = {"slug": ["title"]}


class FieldGroupThroughInline(admin.StackedInline):
    form = forms.FieldGroupThroughAdminForm
    model = models.FieldGroupThrough


class FormFieldGroupAdmin(admin.ModelAdmin):
    form = forms.FormFieldGroupAdminForm
    model = models.FormFieldGroup
    inlines = [FieldGroupThroughInline]


class FormFieldAdmin(admin.ModelAdmin):
    form = forms.FormFieldAdminForm
    model = models.FormField
    inlines = [FieldCustomErrorInline, FieldValidatorInline]
    exclude = ("error_messages", "additional_validators")


admin.site.register(models.Action, ActionModelAdmin)
admin.site.register(models.CleanMethod, CleanMethodModelAdmin)
admin.site.register(models.Validator, ValidatorModelAdmin)
admin.site.register(models.CustomErrorMessage, CustomErrorModelAdmin)
admin.site.register(models.FieldChoice, FieldChoiceModelAdmin)
admin.site.register(models.Form, FormAdmin)
admin.site.register(models.FormData, FormDataAdmin)
admin.site.register(models.FormFieldGroup, FormFieldGroupAdmin)
admin.site.register(models.FormField, FormFieldAdmin)
admin.site.register(models.Wizard, WizardAdmin)
