import os
import shutil
import uuid

from django.conf import settings

from formfactory import models
from formfactory.tests.models import Enum, EnumItem


def cleanup_files():
    test_file_dir = os.path.join(settings.MEDIA_ROOT, "uploads/test")
    shutil.rmtree(test_file_dir, ignore_errors=True)


def load_fixtures(kls):
    kls.form_data = {
        "title": "Form 1",
        "slug": "form-1"
    }
    kls.form = models.Form.objects.create(**kls.form_data)

    kls.fieldchoice_data = {
        "label": "Choice 1",
        "value": "choice-1"
    }
    kls.fieldchoice = models.FieldChoice.objects.create(**kls.fieldchoice_data)

    kls.enum_data = {
        "title": "Enum 1"
    }
    kls.enum = Enum.objects.create(**kls.enum_data)

    kls.enumitem_data = {
        "enum": kls.enum,
        "label": "Choice 2",
        "value": "choice-2"
    }
    kls.enumitem = EnumItem.objects.create(**kls.enumitem_data)

    kls.fieldgroup_data = {
        "title": "Field Group 1",
        "show_title": True
    }
    kls.fieldgroup = models.FormFieldGroup.objects.create(
        **kls.fieldgroup_data
    )

    kls.fieldgroupformthrough_data = {
        "form": kls.form,
        "field_group": kls.fieldgroup,
        "order": 0
    }
    kls.fieldgroupformthrough = models.FieldGroupFormThrough.objects.create(
        **kls.fieldgroupformthrough_data
    )

    for count, field_type in enumerate(models.FIELD_TYPES):
        data = {
            "title": "Form Field %s" % count,
            "slug": "form-field-%s" % count,
            "field_type": field_type[0],
            "label": "Form Field %s" % count,
            "placeholder": "Field Placeholder %s" % count
        }

        # Specialised fields with none default fields will need to have extra
        # data added.
        if field_type[0] == "formfactory.fields.ParagraphField":
            data["paragraph"] = "**formfactory.fields.ParagraphField**"
        setattr(kls, "formfield_data_%s" % count, data)

        if field_type[0] == "django.forms.fields.CharField":
            getattr(kls, "formfield_data_%s" % count)["max_length"] = 100

        setattr(kls, "formfield_%s" % count, models.FormField.objects.create(
            **getattr(kls, "formfield_data_%s" % count)
        ))

        if field_type[0] == "django.forms.fields.ChoiceField":
            getattr(kls, "formfield_%s" % count).choices.add(kls.fieldchoice)
            getattr(kls, "formfield_%s" % count).model_choices = kls.enum

        setattr(kls, "fieldgroupthrough_data_%s" % count, {
            "field_group": kls.fieldgroup,
            "field": getattr(kls, "formfield_%s" % count),
            "order": count
        })
        setattr(
            kls, "fieldgroupthrough_%s" % count,
            models.FieldGroupThrough.objects.create(
                **getattr(kls, "fieldgroupthrough_data_%s" % count)
            )
        )

    kls.simpleform_data = {
        "title": "Subscribe Form",
        "slug": "subscribe-form",
        "success_message": "Success",
        "failure_message": "Failure"
    }
    kls.simpleform = models.Form.objects.create(**kls.simpleform_data)

    kls.simplefieldgroup_data = {
        "title": "Field Group 1",
        "show_title": False
    }
    kls.simplefieldgroup = models.FormFieldGroup.objects.create(
        **kls.simplefieldgroup_data
    )

    kls.simplefieldgroupformthrough_data = {
        "form": kls.simpleform,
        "field_group": kls.simplefieldgroup,
        "order": 0
    }
    kls.simplefieldgroupformthrough = models.FieldGroupFormThrough.objects.create(
        **kls.simplefieldgroupformthrough_data
    )

    kls.action_data = {
        "action": "formfactory.actions.store_data"
    }
    kls.action = models.Action.objects.create(**kls.action_data)

    kls.formactionthrough_data = {
        "action": kls.action,
        "form": kls.simpleform,
        "order": 0
    }
    kls.formactionthrough = models.FormActionThrough.objects.create(
        **kls.formactionthrough_data
    )

    kls.emailaction_data = {
        "action": "formfactory.actions.send_email"
    }
    kls.emailaction = models.Action.objects.create(**kls.emailaction_data)

    kls.emailactionparam_data = [
        {
            "key": "from_email_field",
            "value": "email-address",
            "action": kls.emailaction
        }, {
            "key": "to_email_field",
            "value": "to-email",
            "action": kls.emailaction
        }, {
            "key": "subject_field",
            "value": "subject",
            "action": kls.emailaction
        }
    ]
    for param in kls.emailactionparam_data:
        setattr(
            kls, "emailactionparam_%s" % param["key"],
            models.ActionParam.objects.create(**param)
        )

    kls.emailformactionthrough_data = {
        "action": kls.emailaction,
        "form": kls.simpleform,
        "order": 1
    }
    kls.emailformactionthrough = models.FormActionThrough.objects.create(
        **kls.emailformactionthrough_data
    )

    kls.fileuploadaction_data = {
        "action": "formfactory.actions.file_upload"
    }
    kls.fileuploadaction = models.Action.objects.create(
        **kls.fileuploadaction_data
    )

    kls.fileuploadactionparam_data = [
        {
            "key": "upload_path_field",
            "value": "upload-to",
            "action": kls.fileuploadaction
        }
    ]
    for param in kls.fileuploadactionparam_data:
        setattr(
            kls, "fileuploadactionparam_%s" % param["key"],
            models.ActionParam.objects.create(**param)
        )

    kls.fileuploadformactionthrough_data = {
        "action": kls.fileuploadaction,
        "form": kls.simpleform,
        "order": 2
    }
    kls.fileuploadformactionthrough = models.FormActionThrough.objects.create(
        **kls.fileuploadformactionthrough_data
    )

    kls.simpleformfield_data = {
        "salutation": {
            "title": "Salutation",
            "slug": "salutation",
            "field_type": "django.forms.fields.ChoiceField",
            "label": "Salutation",
            "required": False
        },
        "name": {
            "title": "Name",
            "slug": "name",
            "field_type": "django.forms.fields.CharField",
            "label": "Full Name",
            "required": True
        },
        "email_address": {
            "title": "Email Address",
            "slug": "email-address",
            "field_type": "django.forms.fields.EmailField",
            "label": "Email",
            "help_text": "The email you would like info to be sent to"
        },
        "accept_terms": {
            "title": "Accept Terms",
            "slug": "accept-terms",
            "field_type": "django.forms.fields.BooleanField",
            "label": "Do you accept the terms and conditions",
            "required": False
        },
        "to_email": {
            "title": "To Email",
            "slug": "to-email",
            "field_type": "django.forms.fields.CharField",
            "widget": "django.forms.widgets.HiddenInput",
            "initial": "dev@praekelt.com",
            "required": True
        },
        "id_copy": {
            "title": "ID Copy",
            "slug": "id-copy",
            "field_type": "django.forms.fields.FileField",
            "required": True
        },
        "upload_to": {
            "title": "Upload To",
            "slug": "upload-to",
            "field_type": "django.forms.fields.CharField",
            "widget": "django.forms.widgets.HiddenInput",
            "initial": "uploads/test",
            "required": True
        },
        "subject": {
            "title": "Subject",
            "slug": "subject",
            "field_type": "django.forms.fields.CharField",
            "widget": "django.forms.widgets.HiddenInput",
            "initial": "Test Email",
            "required": True
        },
        "paragraph": {
            "title": "Paragraph",
            "slug": "paragraph",
            "field_type": "formfactory.fields.ParagraphField",
            "paragraph": "**aaaa**"
        }
    }

    count = 0
    for key, value in kls.simpleformfield_data.items():
        setattr(
            kls, "simpleformfield_%s" % key,
            models.FormField.objects.create(**value)
        )

        setattr(kls, "simplefieldgroupthrough_data_%s" % key, {
            "field_group": kls.simplefieldgroup,
            "field": getattr(kls, "simpleformfield_%s" % key),
            "order": count
        })
        setattr(
            kls, "simplefieldgroupthrough_%s" % key,
            models.FieldGroupThrough.objects.create(
                **getattr(kls, "simplefieldgroupthrough_data_%s" % key)
            )
        )

        count += 1

    for salutation in ["Mr", "Mrs", "Dr", "Prof"]:
        choice = models.FieldChoice.objects.create(
            label=salutation, value=salutation
        )
        kls.simpleformfield_salutation.choices.add(choice)

    kls.loginform_data = {
        "title": "Login Form",
        "slug": "login-form",
        "success_message": "Success",
        "failure_message": "Failure",
        "submit_button_text": "Login"
    }
    kls.loginform = models.Form.objects.create(**kls.loginform_data)

    kls.loginfieldgroup_data = {
        "title": "Field Group 1",
        "show_title": True
    }
    kls.loginfieldgroup = models.FormFieldGroup.objects.create(
        **kls.loginfieldgroup_data
    )

    kls.loginfieldgroupformthrough_data = {
        "form": kls.loginform,
        "field_group": kls.loginfieldgroup,
        "order": 0
    }
    kls.loginfieldgroupformthrough = models.FieldGroupFormThrough.objects.create(
        **kls.loginfieldgroupformthrough_data
    )

    kls.loginaction_data = {
        "action": "formfactory.actions.login"
    }
    kls.loginaction = models.Action.objects.create(**kls.loginaction_data)

    kls.loginactionparam_data = [
        {
            "key": "username_field",
            "value": "username",
            "action": kls.loginaction
        }, {
            "key": "password_field",
            "value": "password",
            "action": kls.loginaction
        }
    ]

    for param in kls.loginactionparam_data:
        setattr(
            kls, "loginactionparam_%s" % param["key"],
            models.ActionParam.objects.create(**param)
        )

    kls.loginformactionthrough_data = {
        "action": kls.loginaction,
        "form": kls.loginform,
        "order": 0
    }
    kls.loginformactionthrough = models.FormActionThrough.objects.create(
        **kls.loginformactionthrough_data
    )

    kls.loginformfield_data = {
        "username": {
            "title": "Username",
            "slug": "username",
            "field_type": "django.forms.fields.CharField",
            "label": "Username",
            "required": True
        },
        "password": {
            "title": "Password",
            "slug": "password",
            "field_type": "django.forms.fields.CharField",
            "widget": "django.forms.widgets.PasswordInput",
            "label": "Password",
            "required": True
        }
    }

    count = 0
    for key, value in kls.loginformfield_data.items():
        setattr(
            kls, "loginformfield_%s" % key,
            models.FormField.objects.create(**value)
        )

        setattr(kls, "loginfieldgroupthrough_data_%s" % key, {
            "field_group": kls.loginfieldgroup,
            "field": getattr(kls, "loginformfield_%s" % key),
            "order": count
        })
        setattr(
            kls, "loginfieldgroupthrough_%s" % key,
            models.FieldGroupThrough.objects.create(
                **getattr(kls, "loginfieldgroupthrough_data_%s" % key)
            )
        )

        count += 1

    kls.formdata_data = {
        "uuid": unicode(uuid.uuid4()),
        "form": kls.form
    }
    kls.formdata = models.FormData.objects.create(**kls.formdata_data)

    kls.formdataitem_data = {
        "form_data": kls.formdata,
        "form_field": kls.formfield_1,
        "value": "Form Data Item Value 1"
    }
    kls.formdataitem = models.FormDataItem.objects.create(
        **kls.formdataitem_data
    )
    kls.dummy_validator = "formfactory.tests.validators.dummy_validator"
    kls.dummy_action = "formfactory.tests.actions.dummy_action"

    kls.wizard_data = {
        "title": "Test wizard",
        "slug": "test-wizard",
        "success_message": "Success",
        "failure_message": "Failure",
        "redirect_to": "/"
    }

    kls.validator = models.Validator.objects.create(
        validator=kls.dummy_validator
    )
    kls.wizard = models.Wizard.objects.create(**kls.wizard_data)
    kls.wizardformthrough_simple = models.WizardFormThrough.objects.create(
        wizard=kls.wizard, form=kls.simpleform, order=1
    )
    kls.wizardformthrough_login = models.WizardFormThrough.objects.create(
        wizard=kls.wizard, form=kls.loginform, order=2
    )
