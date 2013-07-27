# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('meet_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('is_pro', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('meet', ['UserProfile'])

        # Adding model 'Event'
        db.create_table('meet_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 26, 0, 0))),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('type_maj', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('type_min', self.gf('django.db.models.fields.CharField')(default='SO', max_length=2)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meet.UserProfile'])),
        ))
        db.send_create_signal('meet', ['Event'])

        # Adding model 'Attendee'
        db.create_table('meet_attendee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meet.Event'])),
            ('usr_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meet.UserProfile'])),
            ('attending', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
        ))
        db.send_create_signal('meet', ['Attendee'])

        # Adding model 'Message'
        db.create_table('meet_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attendee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meet.Attendee'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('contents', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('meet', ['Message'])

        # Adding model 'Event_Action'
        db.create_table('meet_event_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meet.Event'])),
            ('is_Event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('version', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('usr_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meet.Attendee'])),
        ))
        db.send_create_signal('meet', ['Event_Action'])

        # Adding model 'Relationship'
        db.create_table('meet_relationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usr_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meet.UserProfile'])),
            ('friend', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['meet.UserProfile'])),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('meet', ['Relationship'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('meet_userprofile')

        # Deleting model 'Event'
        db.delete_table('meet_event')

        # Deleting model 'Attendee'
        db.delete_table('meet_attendee')

        # Deleting model 'Message'
        db.delete_table('meet_message')

        # Deleting model 'Event_Action'
        db.delete_table('meet_event_action')

        # Deleting model 'Relationship'
        db.delete_table('meet_relationship')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'meet.attendee': {
            'Meta': {'object_name': 'Attendee'},
            'attending': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meet.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usr_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meet.UserProfile']"})
        },
        'meet.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meet.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 26, 0, 0)'}),
            'type_maj': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'type_min': ('django.db.models.fields.CharField', [], {'default': "'SO'", 'max_length': '2'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'meet.event_action': {
            'Meta': {'object_name': 'Event_Action'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meet.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_Event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'usr_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meet.Attendee']"}),
            'version': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'meet.message': {
            'Meta': {'object_name': 'Message'},
            'attendee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meet.Attendee']"}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'meet.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'friend': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['meet.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'usr_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meet.UserProfile']"})
        },
        'meet.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_pro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['meet']