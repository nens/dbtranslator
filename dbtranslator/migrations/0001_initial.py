# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MessageString'
        db.create_table('dbtranslator_messagestring', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('message_id', self.gf('django.db.models.fields.TextField')()),
            ('message_str', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('dbtranslator', ['MessageString'])

        # Adding unique constraint on 'MessageString', fields ['digest', 'language']
        db.create_unique('dbtranslator_messagestring', ['digest', 'language'])


    def backwards(self, orm):
        # Removing unique constraint on 'MessageString', fields ['digest', 'language']
        db.delete_unique('dbtranslator_messagestring', ['digest', 'language'])

        # Deleting model 'MessageString'
        db.delete_table('dbtranslator_messagestring')


    models = {
        'dbtranslator.messagestring': {
            'Meta': {'unique_together': "((u'digest', u'language'),)", 'object_name': 'MessageString'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'message_id': ('django.db.models.fields.TextField', [], {}),
            'message_str': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['dbtranslator']