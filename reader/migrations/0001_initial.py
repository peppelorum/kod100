# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Filter'
        db.create_table('reader_filter', (
            ('regex', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ignore_case', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('filter_on', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('reader', ['Filter'])

        # Adding model 'Category'
        db.create_table('reader_category', (
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('reader', ['Category'])

        # Adding model 'Feed'
        db.create_table('reader_feed', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['reader.Category'])),
            ('feed_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('dt_checked', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('error', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dt_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('reader', ['Feed'])

        # Adding model 'Post'
        db.create_table('reader_post', (
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['reader.Feed'])),
            ('current', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('dt_cached', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('dt_published', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=512)),
            ('guid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('saved', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('reader', ['Post'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Filter'
        db.delete_table('reader_filter')

        # Deleting model 'Category'
        db.delete_table('reader_category')

        # Deleting model 'Feed'
        db.delete_table('reader_feed')

        # Deleting model 'Post'
        db.delete_table('reader_post')
    
    
    models = {
        'reader.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        'reader.feed': {
            'Meta': {'object_name': 'Feed'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['reader.Category']"}),
            'dt_checked': ('django.db.models.fields.DateTimeField', [], {}),
            'dt_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'error': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'reader.filter': {
            'Meta': {'object_name': 'Filter'},
            'filter_on': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_case': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'regex': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'reader.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'dt_cached': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dt_published': ('django.db.models.fields.DateTimeField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['reader.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '512'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'saved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }
    
    complete_apps = ['reader']
