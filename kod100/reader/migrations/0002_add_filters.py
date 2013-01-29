# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding M2M table for field filters on 'Feed'
        db.create_table('reader_feed_filters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm['reader.feed'], null=False)),
            ('filter', models.ForeignKey(orm['reader.filter'], null=False))
        ))
        db.create_unique('reader_feed_filters', ['feed_id', 'filter_id'])
    
    
    def backwards(self, orm):
        
        # Removing M2M table for field filters on 'Feed'
        db.delete_table('reader_feed_filters')
    
    
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
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reader.Filter']", 'null': 'True', 'blank': 'True'}),
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
