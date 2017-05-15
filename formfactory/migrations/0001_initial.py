# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FormData'
        db.create_table(u'formfactory_formdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.Form'])),
        ))
        db.send_create_signal(u'formfactory', ['FormData'])

        # Adding model 'FormDataItem'
        db.create_table(u'formfactory_formdataitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form_data', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['formfactory.FormData'])),
            ('form_field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.FormField'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'formfactory', ['FormDataItem'])

        # Adding model 'Action'
        db.create_table(u'formfactory_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'formfactory', ['Action'])

        # Adding model 'Validator'
        db.create_table(u'formfactory_validator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('validator', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'formfactory', ['Validator'])

        # Adding model 'CleanMethod'
        db.create_table(u'formfactory_cleanmethod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clean_method', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'formfactory', ['CleanMethod'])

        # Adding model 'CustomErrorMessage'
        db.create_table(u'formfactory_customerrormessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'formfactory', ['CustomErrorMessage'])

        # Adding model 'ActionParam'
        db.create_table(u'formfactory_actionparam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='params', to=orm['formfactory.Action'])),
        ))
        db.send_create_signal(u'formfactory', ['ActionParam'])

        # Adding model 'FormActionThrough'
        db.create_table(u'formfactory_formactionthrough', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.Action'])),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.Form'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'formfactory', ['FormActionThrough'])

        # Adding model 'Form'
        db.create_table(u'formfactory_form', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=256)),
            ('success_message', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('failure_message', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('redirect_to', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('clean_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.CleanMethod'], null=True, blank=True)),
            ('submit_button_text', self.gf('django.db.models.fields.CharField')(default='Submit', max_length=64)),
            ('enable_csrf', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'formfactory', ['Form'])

        # Adding model 'Wizard'
        db.create_table(u'formfactory_wizard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=256)),
            ('success_message', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('failure_message', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('redirect_to', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'formfactory', ['Wizard'])

        # Adding model 'WizardFormThrough'
        db.create_table(u'formfactory_wizardformthrough', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wizard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.Wizard'])),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.Form'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'formfactory', ['WizardFormThrough'])

        # Adding model 'WizardActionThrough'
        db.create_table(u'formfactory_wizardactionthrough', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.Action'])),
            ('wizard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.Wizard'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'formfactory', ['WizardActionThrough'])

        # Adding model 'FieldChoice'
        db.create_table(u'formfactory_fieldchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'formfactory', ['FieldChoice'])

        # Adding model 'FormFieldGroup'
        db.create_table(u'formfactory_formfieldgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('show_title', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'formfactory', ['FormFieldGroup'])

        # Adding model 'FieldGroupFormThrough'
        db.create_table(u'formfactory_fieldgroupformthrough', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.FormFieldGroup'])),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.Form'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'formfactory', ['FieldGroupFormThrough'])

        # Adding model 'FormField'
        db.create_table(u'formfactory_formfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=256)),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('widget', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('initial', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('max_length', self.gf('django.db.models.fields.PositiveIntegerField')(default=256, null=True, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('placeholder', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('disabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('model_choices_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('model_choices_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'formfactory', ['FormField'])

        # Adding M2M table for field choices on 'FormField'
        m2m_table_name = db.shorten_name(u'formfactory_formfield_choices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('formfield', models.ForeignKey(orm[u'formfactory.formfield'], null=False)),
            ('fieldchoice', models.ForeignKey(orm[u'formfactory.fieldchoice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['formfield_id', 'fieldchoice_id'])

        # Adding M2M table for field additional_validators on 'FormField'
        m2m_table_name = db.shorten_name(u'formfactory_formfield_additional_validators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('formfield', models.ForeignKey(orm[u'formfactory.formfield'], null=False)),
            ('validator', models.ForeignKey(orm[u'formfactory.validator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['formfield_id', 'validator_id'])

        # Adding M2M table for field error_messages on 'FormField'
        m2m_table_name = db.shorten_name(u'formfactory_formfield_error_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('formfield', models.ForeignKey(orm[u'formfactory.formfield'], null=False)),
            ('customerrormessage', models.ForeignKey(orm[u'formfactory.customerrormessage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['formfield_id', 'customerrormessage_id'])

        # Adding model 'FieldGroupThrough'
        db.create_table(u'formfactory_fieldgroupthrough', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.FormField'])),
            ('field_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formfactory.FormFieldGroup'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'formfactory', ['FieldGroupThrough'])


    def backwards(self, orm):
        # Deleting model 'FormData'
        db.delete_table(u'formfactory_formdata')

        # Deleting model 'FormDataItem'
        db.delete_table(u'formfactory_formdataitem')

        # Deleting model 'Action'
        db.delete_table(u'formfactory_action')

        # Deleting model 'Validator'
        db.delete_table(u'formfactory_validator')

        # Deleting model 'CleanMethod'
        db.delete_table(u'formfactory_cleanmethod')

        # Deleting model 'CustomErrorMessage'
        db.delete_table(u'formfactory_customerrormessage')

        # Deleting model 'ActionParam'
        db.delete_table(u'formfactory_actionparam')

        # Deleting model 'FormActionThrough'
        db.delete_table(u'formfactory_formactionthrough')

        # Deleting model 'Form'
        db.delete_table(u'formfactory_form')

        # Deleting model 'Wizard'
        db.delete_table(u'formfactory_wizard')

        # Deleting model 'WizardFormThrough'
        db.delete_table(u'formfactory_wizardformthrough')

        # Deleting model 'WizardActionThrough'
        db.delete_table(u'formfactory_wizardactionthrough')

        # Deleting model 'FieldChoice'
        db.delete_table(u'formfactory_fieldchoice')

        # Deleting model 'FormFieldGroup'
        db.delete_table(u'formfactory_formfieldgroup')

        # Deleting model 'FieldGroupFormThrough'
        db.delete_table(u'formfactory_fieldgroupformthrough')

        # Deleting model 'FormField'
        db.delete_table(u'formfactory_formfield')

        # Removing M2M table for field choices on 'FormField'
        db.delete_table(db.shorten_name(u'formfactory_formfield_choices'))

        # Removing M2M table for field additional_validators on 'FormField'
        db.delete_table(db.shorten_name(u'formfactory_formfield_additional_validators'))

        # Removing M2M table for field error_messages on 'FormField'
        db.delete_table(db.shorten_name(u'formfactory_formfield_error_messages'))

        # Deleting model 'FieldGroupThrough'
        db.delete_table(u'formfactory_fieldgroupthrough')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'formfactory.action': {
            'Meta': {'object_name': 'Action'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'formfactory.actionparam': {
            'Meta': {'object_name': 'ActionParam'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'params'", 'to': u"orm['formfactory.Action']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'formfactory.cleanmethod': {
            'Meta': {'object_name': 'CleanMethod'},
            'clean_method': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'formfactory.customerrormessage': {
            'Meta': {'object_name': 'CustomErrorMessage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'formfactory.fieldchoice': {
            'Meta': {'ordering': "['label']", 'object_name': 'FieldChoice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'formfactory.fieldgroupformthrough': {
            'Meta': {'ordering': "['order']", 'object_name': 'FieldGroupFormThrough'},
            'field_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.FormFieldGroup']"}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'formfactory.fieldgroupthrough': {
            'Meta': {'ordering': "['order']", 'object_name': 'FieldGroupThrough'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.FormField']"}),
            'field_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.FormFieldGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'formfactory.form': {
            'Meta': {'ordering': "['title']", 'object_name': 'Form'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['formfactory.Action']", 'through': u"orm['formfactory.FormActionThrough']", 'symmetrical': 'False'}),
            'clean_method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.CleanMethod']", 'null': 'True', 'blank': 'True'}),
            'enable_csrf': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'failure_message': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'redirect_to': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '256'}),
            'submit_button_text': ('django.db.models.fields.CharField', [], {'default': "'Submit'", 'max_length': '64'}),
            'success_message': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'formfactory.formactionthrough': {
            'Meta': {'ordering': "['order']", 'object_name': 'FormActionThrough'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.Action']"}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'formfactory.formdata': {
            'Meta': {'ordering': "['uuid']", 'object_name': 'FormData'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        u'formfactory.formdataitem': {
            'Meta': {'object_name': 'FormDataItem'},
            'form_data': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['formfactory.FormData']"}),
            'form_field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.FormField']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'formfactory.formfield': {
            'Meta': {'object_name': 'FormField'},
            'additional_validators': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['formfactory.Validator']", 'symmetrical': 'False', 'blank': 'True'}),
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['formfactory.FieldChoice']", 'null': 'True', 'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'error_messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['formfactory.CustomErrorMessage']", 'symmetrical': 'False', 'blank': 'True'}),
            'field_groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fields'", 'symmetrical': 'False', 'through': u"orm['formfactory.FieldGroupThrough']", 'to': u"orm['formfactory.FormFieldGroup']"}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'max_length': ('django.db.models.fields.PositiveIntegerField', [], {'default': '256', 'null': 'True', 'blank': 'True'}),
            'model_choices_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'model_choices_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'widget': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'formfactory.formfieldgroup': {
            'Meta': {'object_name': 'FormFieldGroup'},
            'forms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fieldgroups'", 'symmetrical': 'False', 'through': u"orm['formfactory.FieldGroupFormThrough']", 'to': u"orm['formfactory.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show_title': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'formfactory.validator': {
            'Meta': {'object_name': 'Validator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'validator': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'formfactory.wizard': {
            'Meta': {'object_name': 'Wizard'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['formfactory.Action']", 'through': u"orm['formfactory.WizardActionThrough']", 'symmetrical': 'False'}),
            'failure_message': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'forms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['formfactory.Form']", 'through': u"orm['formfactory.WizardFormThrough']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'redirect_to': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '256'}),
            'success_message': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'formfactory.wizardactionthrough': {
            'Meta': {'ordering': "['order']", 'object_name': 'WizardActionThrough'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.Action']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'wizard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.Wizard']"})
        },
        u'formfactory.wizardformthrough': {
            'Meta': {'ordering': "['order']", 'object_name': 'WizardFormThrough'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'wizard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formfactory.Wizard']"})
        }
    }

    complete_apps = ['formfactory']