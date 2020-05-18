# Generated by Django 2.2.10 on 2020-05-14 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Metafield',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The time this record was firstly created. Do not modify.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Automatically updated each time the record is saved.')),
                ('editedrecord', models.BooleanField(default=False, help_text='Tick to indicate that this record has been finalized', verbose_name='edited record?')),
                ('review', models.BooleanField(default=False, help_text='Tick to indicate that this record is under review by the editorial team', verbose_name='review')),
                ('internal_notes', models.TextField(blank=True, verbose_name='internal_notes')),
                ('isprivate', models.BooleanField(blank=True, default=False, verbose_name='is private')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('source', models.CharField(max_length=200, verbose_name='source')),
                ('desc', models.TextField(verbose_name='desc')),
                ('solr_field', models.CharField(blank=True, max_length=350, verbose_name='solr_field')),
                ('deprecated', models.BooleanField(default=False, help_text='deprecated', verbose_name='deprecated?')),
                ('created_by', models.ForeignKey(blank=True, help_text='No need to edit: automatically set when saving', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_metafield', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, help_text='No need to edit: automatically set when saving', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_metafield', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Metafield',
                'verbose_name_plural': 'Metafields',
                'ordering': ['source', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Implementation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The time this record was firstly created. Do not modify.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Automatically updated each time the record is saved.')),
                ('editedrecord', models.BooleanField(default=False, help_text='Tick to indicate that this record has been finalized', verbose_name='edited record?')),
                ('review', models.BooleanField(default=False, help_text='Tick to indicate that this record is under review by the editorial team', verbose_name='review')),
                ('internal_notes', models.TextField(blank=True, verbose_name='internal_notes')),
                ('isprivate', models.BooleanField(blank=True, default=False, verbose_name='is private')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('platform', models.CharField(max_length=200, verbose_name='platform')),
                ('field_type', models.CharField(blank=True, max_length=200, verbose_name='field_type')),
                ('profile', models.CharField(blank=True, max_length=200, verbose_name='profile')),
                ('solr_field', models.CharField(blank=True, max_length=350, verbose_name='solr_field')),
                ('deprecated', models.BooleanField(default=False, help_text='deprecated', verbose_name='deprecated?')),
                ('created_by', models.ForeignKey(blank=True, help_text='No need to edit: automatically set when saving', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_implementation', to=settings.AUTH_USER_MODEL)),
                ('metafield', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metamodel.Metafield')),
                ('updated_by', models.ForeignKey(blank=True, help_text='No need to edit: automatically set when saving', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_implementation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Implementation',
                'verbose_name_plural': 'Implementations',
                'ordering': ['platform', 'name'],
            },
        ),
    ]
