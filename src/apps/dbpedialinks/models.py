from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib import admin

import datetime

# See also: https://docs.djangoproject.com/en/1.10/topics/migrations/#workflow


class SGDocument(models.Model):
    """Model definition for SGDocument."""

    title = models.CharField(max_length=250, verbose_name="title", null=True, blank=True,)
    uri = models.URLField(max_length=300)

    author = models.CharField(blank=True, max_length=200, verbose_name="author")
    pubyear = models.IntegerField(blank=True, null=True, verbose_name="publication year", help_text="")
    description = models.TextField(blank=True, verbose_name="description (put everything in here for now)")

    dbentities = models.ManyToManyField('DBPediaEntity')

    class Meta:
        """Meta definition for SGDocument."""

        verbose_name = 'SGDocument'
        verbose_name_plural = 'SGDocuments'
        ordering = ["uri"]

    def __unicode__(self):
        """Unicode representation of SGDocument."""
        return self.uri

    class Admin(admin.ModelAdmin):
        list_display = ('id', 'title', 'uri')
        search_fields = ['id', 'title', 'uri']



class DBPediaEntity(models.Model):
    """Model definition for DBPediaEntity."""

    title = models.CharField(max_length=250, verbose_name="title", null=True, blank=True,)
    uri = models.URLField(max_length=300)

    totarticles = models.IntegerField(null=True, blank=True, verbose_name="Tot associated articles")
    dbtype = models.CharField(blank=True, max_length=200, verbose_name="dbtype")

    description = models.TextField(blank=True, verbose_name="description (put everything in here for now)")

    class Meta:
        """Meta definition for DBPediaEntity."""

        verbose_name = 'DBPedia Entity'
        verbose_name_plural = 'DBPedia Entities'
        ordering = ["title"]

    def __unicode__(self):
        """Unicode representation of DBPediaEntity."""
        return self.uri

    def update_tot_count(self):
        self.totarticles = self.sgdocument_set.count()
        self.save()

    class Admin(admin.ModelAdmin):
        list_display = ('id', 'title', 'uri')
        search_fields = ['id', 'title', 'uri']

