from django.core.management.base import BaseCommand, CommandError
from metamodel.models import *
import csv


class Command(BaseCommand):
	help = 'Load ghseet export into DB - overwrite by default'

	def add_arguments(self, parser):
		parser.add_argument('filename', type=str)

	def handle(self, *args, **options):
		filename = options['filename']

		if True:
			self.stdout.write("++ = ++ = ++ = ++ Cleaning all previously saved contents ....")
			Metafield.objects.all().delete()
			self.stdout.write(".........successfully erased all previously saved contents!\n")
			# pass # nothing to delete


		print(filename)

		f = open(filename, 'rU') # rU http://www.gossamer-threads.com/lists/python/dev/723649

		# bag = []
		self.stdout.write("Reading...")
		try:
			reader = csv.DictReader(f)
			for row in reader:
				write_record(row)
		finally:
			f.close()


#  helper for django models
def get_or_new(model, name, source):
	"""helper method"""
	try:
		# if there's an object with same name, we keep that one!
		obj = model.objects.get(name=name, source=source)
		print("++++++++++++++++++++++++++ found existing obj:	%s"	 % (obj))
	except:
		obj = model(name=name, source=source)
		obj.save()
		print("======= created new obj:	  %s"  % (obj))
	return obj


def get_or_new_related(model, name, platform):
	"""helper method"""
	try:
		# if there's an object with same name, we keep that one!
		obj = model.objects.get(name=name, platform=platform)
		print("++++++++++++++++++++++++++ found existing obj:	%s"	 % (obj))
	except:
		obj = model(name=name, platform=platform)
		obj.save()
		print("======= created new obj:	  %s"  % (obj))
	return obj



def get_main_title(row):
	ids_fields = [ "dsl_field_name", "webapp display name",  "gbq_field_name", "bulkdata_field_name"]
	for x in ids_fields:
		test = row[x].strip()
		if test:
			return row[x]


def write_record(row):
	"write a record to DB"
	main_title = get_main_title(row)
	main_source = row['source_name']
	if main_title and main_source:
		print(main_source, main_title)
		obj = get_or_new(Metafield, main_title, main_source)
		obj.solr_field = row['solr_field']
		obj.source = row['source_name']
		obj.desc = row['dsl_description']

		obj.save()

		if row["dsl_field_name"]:
			rel1 = get_or_new_related(Implementation, row["dsl_field_name"], "dsl")
			rel1.metafield = obj
			rel1.save()

		if row["webapp display name"]:
			rel1 = get_or_new_related(Implementation, row["dsl_field_name"], "webapp")
			rel1.metafield = obj
			rel1.field_type = row['dsl_field_type']
			rel1.save()

		if row["gbq_field_name"]:
			rel1 = get_or_new_related(Implementation, row["gbq_field_name"], "gbq")
			rel1.metafield = obj
			rel1.field_type = row['bulkdata_field_type']
			rel1.save()

		if row["bulkdata_field_name"]:
			rel1 = get_or_new_related(Implementation, row["bulkdata_field_name"], "bulkd")
			rel1.metafield = obj
			rel1.field_type = row['gbq_field_type']
			rel1.save()


	