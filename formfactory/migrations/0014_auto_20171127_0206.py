# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-27 02:06
from __future__ import unicode_literals

from django.db import migrations, models
import simplemde.fields


class Migration(migrations.Migration):

    dependencies = [
        ('formfactory', '0013_auto_20171124_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='formfield',
            name='paragraph',
            field=simplemde.fields.SimpleMDEField(blank=True, help_text=b'Markdown for the formfactory ParagraphField and ParagraphWidget combination.', null=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='action',
            field=models.CharField(choices=[(b'formfactory.actions.send_email', b'formfactory.actions.send_email'), (b'formfactory.actions.file_upload', b'formfactory.actions.file_upload'), (b'formfactory.tests.actions.dummy_wizard_action', b'formfactory.tests.actions.dummy_wizard_action'), (b'formfactory.actions.store_data', b'formfactory.actions.store_data'), (b'formfactory.tests.actions.dummy_action', b'formfactory.tests.actions.dummy_action'), (b'formfactory.actions.login', b'formfactory.actions.login')], max_length=128),
        ),
        migrations.AlterField(
            model_name='cleanmethod',
            name='clean_method',
            field=models.CharField(choices=[(b'formfactory.tests.clean_methods.check_if_values_match', b'formfactory.tests.clean_methods.check_if_values_match')], max_length=128),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='field_type',
            field=models.CharField(choices=[(b'django.forms.fields.BooleanField', b'BooleanField'), (b'django.forms.fields.CharField', b'CharField'), (b'django.forms.fields.ChoiceField', b'ChoiceField'), (b'django.forms.fields.DateField', b'DateField'), (b'django.forms.fields.DateTimeField', b'DateTimeField'), (b'django.forms.fields.DecimalField', b'DecimalField'), (b'django.forms.fields.EmailField', b'EmailField'), (b'django.forms.fields.FileField', b'FileField'), (b'django.forms.fields.FloatField', b'FloatField'), (b'django.forms.fields.GenericIPAddressField', b'GenericIPAddressField'), (b'django.forms.fields.IntegerField', b'IntegerField'), (b'django.forms.fields.MultipleChoiceField', b'MultipleChoiceField'), (b'django.forms.fields.SlugField', b'SlugField'), (b'django.forms.fields.SplitDateTimeField', b'SplitDateTimeField'), (b'django.forms.fields.TimeField', b'TimeField'), (b'django.forms.fields.URLField', b'URLField'), (b'django.forms.fields.UUIDField', b'UUIDField'), (b'formfactory.fields.ParagraphField', b'ParagraphField')], max_length=128),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='widget',
            field=models.CharField(blank=True, choices=[(b'django.forms.widgets.CheckboxInput', b'CheckboxInput'), (b'django.forms.widgets.CheckboxSelectMultiple', b'CheckboxSelectMultiple'), (b'django.forms.widgets.DateInput', b'DateInput'), (b'django.forms.widgets.DateTimeInput', b'DateTimeInput'), (b'django.forms.widgets.EmailInput', b'EmailInput'), (b'django.forms.widgets.FileInput', b'FileInput'), (b'django.forms.widgets.HiddenInput', b'HiddenInput'), (b'django.forms.widgets.NullBooleanSelect', b'NullBooleanSelect'), (b'django.forms.widgets.NumberInput', b'NumberInput'), (b'django.forms.widgets.PasswordInput', b'PasswordInput'), (b'django.forms.widgets.RadioSelect', b'RadioSelect'), (b'django.forms.widgets.Select', b'Select'), (b'django.forms.widgets.SelectMultiple', b'SelectMultiple'), (b'django.forms.widgets.Textarea', b'Textarea'), (b'django.forms.widgets.TextInput', b'TextInput'), (b'django.forms.widgets.TimeInput', b'TimeInput'), (b'django.forms.widgets.URLInput', b'URLInput'), (b'formfactory.widgets.ParagraphWidget', b'ParagraphWidget')], help_text='Leave blank if you prefer to use the default widget.', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='validator',
            name='validator',
            field=models.CharField(choices=[(b'formfactory.tests.validators.dummy_validator', b'formfactory.tests.validators.dummy_validator')], max_length=128),
        ),
    ]