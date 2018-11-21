# HOW TO

# https://docs.djangoproject.com/en/1.10/howto/custom-management-commands/

# python manage.py tags_totcount

import sys
from django.core.management.base import BaseCommand

from dbpedialinks.models import *
from myutils.myutils import *


class Command(BaseCommand):
    help = 'command to calc tot counts for tags / so to make tagcloud faster'

    def handle(self, *args, **options):
        tot = DBPediaEntity.objects.count()
        counter = 0
        for x in DBPediaEntity.objects.all():
            counter += 1
            x.update_tot_count()
            print("{}/{} - {}".format(counter, tot, x.title))

        print("Done - objects created!")
