from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib import admin
from collections import Counter

import datetime

# See also: https://docs.djangoproject.com/en/1.10/topics/migrations/#workflow


class SGDocument(models.Model):
    """Model definition for SGDocument."""

    title = models.CharField(
        max_length=250,
        verbose_name="title",
        null=True,
        blank=True,
    )
    uri = models.URLField(max_length=300)

    author = models.CharField(
        blank=True, max_length=200, verbose_name="author")
    pubyear = models.IntegerField(
        blank=True, null=True, verbose_name="publication year", help_text="")
    description = models.TextField(
        blank=True,
        verbose_name="description (put everything in here for now)")

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

    title = models.CharField(
        max_length=250,
        verbose_name="title",
        null=True,
        blank=True,
    )
    uri = models.URLField(max_length=300)

    totarticles = models.IntegerField(
        null=True, blank=True, verbose_name="Tot associated articles")
    dbtype = models.CharField(
        blank=True, max_length=200, verbose_name="dbtype")

    description = models.TextField(
        blank=True,
        verbose_name="description (put everything in here for now)")

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

    def related_subjects(self, size=99999999, articles_set=None):
        """calc co-occurring subjects across whole publications; returns a dict object containing only subjects with a minimum number of objects:

        <articles_set> : allows to pass manually a queryset for extracting co-occurrence data

        >>> c
        Counter({<DBPediaEntity: DBPediaEntity object (83510)>: 1, <DBPediaEntity: DBPediaEntity object (74073)>: 1, <DBPediaEntity: DBPediaEntity object (78827)>: 1, <DBPediaEntity: DBPediaEntity object (62890)>: 1})
        >>> [x for x in c.items()]
        [(<DBPediaEntity: DBPediaEntity object (83510)>, 1), (<DBPediaEntity: DBPediaEntity object (74073)>, 1), (<DBPediaEntity: DBPediaEntity object (78827)>, 1), (<DBPediaEntity: DBPediaEntity object (62890)>, 1)]
        >>> [x[0].title for x in c.items()]
        ['Body area network', 'Carrier-sense multiple access with collision avoidance', 'Probability-generating function', 'Queueing theory']
        
        """

        def count_and_reduce_manually(lista, minim):
            """reduce by providing a min count / not good as it can return too many results"""
            c = Counter(lista)
            out = {}
            for x in c.items():
                if x[1] >= minim:
                    out[x[0]] = x[1]
            return out

        def count_and_reduce(lista, size):
            "reduce by taking first N elements sorted by tot count"
            c = Counter(lista)
            out = c.items()
            out = sorted(out, key=lambda t: (t[1], t[0].title), reverse=True)
            return out[:size]

        if not articles_set:
            articles_set = self.sgdocument_set.all()
        # approach 1: use co-occurrnce to define relatedness
        # one level recursion - takes a long time so should be precalculated
        # also this produces way too many results
        related = []
        for a in articles_set:
            related += a.dbentities.exclude(id=self.id)
        out = count_and_reduce(related, size)
        print("Found:", len(out))

        if False:  # 2nd iteration
            # DOESNT WORK cause we need to output a graph with multiple nodes!
            seed, related = out.keys(), []
            for subj in seed:
                print("second iteration for", subj)
                for a2 in subj.sgdocument_set.all():
                    related += a2.dbentities.exclude(id=self.id)
            related += seed
            print("..reducing now....")
            out = count_and_reduce(related, 2)
        # finally return a dict
        return out

        # approach #2: use tot articles to take to 10 subjects
        # TODO

    class Admin(admin.ModelAdmin):
        list_display = ('id', 'title', 'uri')
        search_fields = ['id', 'title', 'uri']
