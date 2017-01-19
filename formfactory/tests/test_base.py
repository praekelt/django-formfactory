import uuid

from formfactory import models


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

    for count, field_type in enumerate(models.FIELD_TYPES):
        setattr(kls, "formfield_data_%s" % count, {
            "title": "Form Field %s" % count,
            "slug": "form-field-%s" % count,
            "position": count,
            "form": kls.form,
            "field_type": field_type[0],
            "label": "Form Field %s" % count,
            "placeholder": "Field Placeholder %s" % count
        })

        if field_type[0] == "CharField":
            getattr(kls, "formfield_data_%s" % count)["max_length"] = 100

        setattr(kls, "formfield_%s" % count, models.FormField.objects.create(
            **getattr(kls, "formfield_data_%s" % count)
        ))

        if field_type[0] == "ChoiceField":
            getattr(kls, "formfield_%s" % count).choices.add(kls.fieldchoice)

    kls.simpleform_data = {
        "title": "Subscribe Form",
        "slug": "subscribe-form",
        "success_message": "Success",
        "failure_message": "Failure"
    }
    kls.simpleform = models.Form.objects.create(**kls.simpleform_data)

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

    kls.simpleformfield_data = {
        "salutation": {
            "title": "Salutation",
            "slug": "salutation",
            "position": 0,
            "form": kls.simpleform,
            "field_type": "ChoiceField",
            "label": "Salutation",
            "required": False
        },
        "name": {
            "title": "Name",
            "slug": "name",
            "position": 1,
            "form": kls.simpleform,
            "field_type": "CharField",
            "label": "Full Name",
            "required": True
        },
        "email_address": {
            "title": "Email Address",
            "slug": "email-address",
            "position": 2,
            "form": kls.simpleform,
            "field_type": "EmailField",
            "label": "Email",
            "help_text": "The email you would like info to be sent to"
        },
        "accept_terms": {
            "title": "Accept Terms",
            "slug": "accept-terms",
            "position": 3,
            "form": kls.simpleform,
            "field_type": "BooleanField",
            "label": "Do you accept the terms and conditions",
            "required": False
        },
        "to_email": {
            "title": "To Email",
            "slug": "to-email",
            "position": 4,
            "form": kls.simpleform,
            "field_type": "CharField",
            "widget": "HiddenInput",
            "initial": "dev@praekelt.com",
            "required": True
        },
        "subject": {
            "title": "Subject",
            "slug": "subject",
            "position": 5,
            "form": kls.simpleform,
            "field_type": "CharField",
            "widget": "HiddenInput",
            "initial": "Test Email",
            "required": True
        }
    }
    for key, value in kls.simpleformfield_data.items():
        setattr(
            kls, "simpleformfield_%s" % key,
            models.FormField.objects.create(**value)
        )

    for salutation in ["Mr", "Mrs", "Dr", "Prof"]:
        choice = models.FieldChoice.objects.create(
            label=salutation, value=salutation
        )
        kls.simpleformfield_salutation.choices.add(choice)

    kls.loginform_data = {
        "title": "Login Form",
        "slug": "login-form",
        "success_message": "Success",
        "failure_message": "Failure"
    }
    kls.loginform = models.Form.objects.create(**kls.loginform_data)

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
            "position": 0,
            "form": kls.loginform,
            "field_type": "CharField",
            "label": "Username",
            "required": True
        },
        "password": {
            "title": "Password",
            "slug": "password",
            "position": 1,
            "form": kls.loginform,
            "field_type": "CharField",
            "widget": "PasswordInput",
            "label": "Password",
            "required": True
        }
    }
    for key, value in kls.loginformfield_data.items():
        setattr(
            kls, "loginformfield_%s" % key,
            models.FormField.objects.create(**value)
        )

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

    wizard_data = {
        "title": "Test wizard",
        "slug": "test-wizard",
        "success_message": "Success",
        "failure_message": "Failure",
        "redirect_to": "/"
    }

    # create wizard
    kls.wizard = models.Wizard.objects.create(**wizard_data)

    # add forms to the wizard
    models.FormOrderThrough.objects.create(
        wizard=kls.wizard, form=kls.simpleform, order=1
    )
    models.FormOrderThrough.objects.create(
        wizard=kls.wizard, form=kls.loginform, order=2
    )
