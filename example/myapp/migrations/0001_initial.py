# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FineFile'
        db.create_table(u'myapp_finefile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('fine_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'myapp', ['FineFile'])


    def backwards(self, orm):
        # Deleting model 'FineFile'
        db.delete_table(u'myapp_finefile')


    models = {
        u'myapp.finefile': {
            'Meta': {'object_name': 'FineFile'},
            'fine_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['myapp']