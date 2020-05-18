from __future__ import unicode_literals

from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


import datetime
# 
import myutils.abstract_models as mymodels




class Implementation(mymodels.EnhancedModel):
	"""(Implementation enhanced model - timestamps and creation fields inherited)"""
	
	name = models.CharField(max_length=200, verbose_name="name")
	platform = models.CharField(max_length=200, verbose_name="platform", 
		choices=[('dsl', 'DSL'), ('gbq', 'GBQ'), ('bulkd', 'Bulk Data'), ('webapp', 'Web App')])
	field_type = models.CharField(blank=True, max_length=200, verbose_name="field_type",)
		# choices=[('string', 'string'), ('integer', 'integer'), ('JSON', 'JSON'), ('nested_list', 'nested_list')])
	profile = models.CharField(blank=True, max_length=200, verbose_name="profile / visibility",
		choices=[('public', 'public'), ('private', 'private'), ('NIH', 'NIH'), ('hidden', 'hidden')])
	solr_field = models.CharField(blank=True, max_length=350, verbose_name="solr_field")
	deprecated = models.BooleanField(default=False, verbose_name="deprecated?", help_text="deprecated")

	metafield = models.ForeignKey('Metafield', blank=True, null=True, on_delete=models.CASCADE)

	
	class Admin(admin.ModelAdmin):
		readonly_fields=('created_at', 'updated_at')
		list_display = ('id', 'name', 'platform', 'solr_field', 'updated_at')
		list_display_links = ('id', 'name',)
		search_fields = ['id', 'name', 'desc']
		list_filter = ('created_at', 'updated_at', 'created_by', 'editedrecord', 'review', 'platform', 'deprecated')
		#filter_horizontal = (,) 
		#related_search_fields = { 'fieldname': ('searchattr_name',)}
		#inlines = (inlineModel1, inlineModel2)
		fieldsets = [
			('Administration',	
				{'fields':	
					['editedrecord', 'review', 'internal_notes', ('created_at', 'created_by'), 
					  ('updated_at', 'updated_by')
					 ],	 
				'classes': ['collapse']
				}),
			('',	
				{'fields':	
					['name', 'platform', 'field_type', 'profile', 'solr_field', 'deprecated', 
					 ],	 
				# 'classes': ['collapse']
				}),	
			]
		# class Media:
		# 	js = ("js/admin_fixes/fix_fields_size.js",)
			
		def save_model(self, request, obj, form, change):
			"""adds the user information when the rec is saved"""
			if getattr(obj, 'created_by', None) is None:
				  obj.created_by = request.user
			obj.updated_by = request.user
			obj.save()	
			
			
	class Meta:
		verbose_name_plural="Implementations"
		verbose_name = "Implementation"
		ordering = ["platform", "name"]
		
	def __unicode__(self):
		return "Implementation %d: %s" % (self.id, self.name)
	



class ImplementationInline(admin.TabularInline): # StackedInline
	model = Implementation
	fields = ('platform', 'name', 'field_type', 'profile', 'solr_field', 'deprecated')
	# radio_fields = {"platform": admin.HORIZONTAL}





class Metafield(mymodels.EnhancedModel):
	"""(Metafield enhanced model - timestamps and creation fields inherited)"""
	
	name = models.CharField(max_length=200, verbose_name="name")
	source = models.CharField(max_length=200, verbose_name="source", 
		choices=[('publications', 'publications'), ('grants', 'grants'), ('patents', 'patents'), 
					('clinical_trials', 'clinical_trials'), ('policy_documents', 'policy_documents'), 
					('researchers', 'researchers'), ('organizations', 'organizations'), 
					('datasets', 'datasets'),
					])
	desc = models.TextField(verbose_name="desc")
	solr_field = models.CharField(blank=True, max_length=350, verbose_name="solr_field")
	deprecated = models.BooleanField(default=False, verbose_name="deprecated?", help_text="deprecated")

	
	class Admin(admin.ModelAdmin):
		readonly_fields=('created_at', 'updated_at')
		list_display = ('id', 'name', 'source', 'solr_field', 'updated_at')
		list_display_links = ('id', 'name',)
		search_fields = ['id', 'name', 'desc']
		list_filter = ('updated_at', 'updated_by', 'review', 'source', 'deprecated')
		radio_fields = {"source": admin.VERTICAL}
		#filter_horizontal = (,) 
		#related_search_fields = { 'fieldname': ('searchattr_name',)}
		inlines = [
			ImplementationInline,
		]
		fieldsets = [
			('Administration',	
				{'fields':	
					['editedrecord', 'review', 'internal_notes', ('created_at', 'created_by'), 
					  ('updated_at', 'updated_by')
					 ],	 
				'classes': ['collapse']
				}),
			('Shared Field Information',	
				{'fields':	
					[('name', 'deprecated'), 'source', 'desc', 'solr_field', 
					 ],	 
				# 'classes': ['collapse']
				}),	
			]
		#class Media:
			#js = ("js/admin_fixes/fix_fields_size.js",)
			
		def save_model(self, request, obj, form, change):
			"""adds the user information when the rec is saved"""
			if getattr(obj, 'created_by', None) is None:
				  obj.created_by = request.user
			obj.updated_by = request.user
			obj.save()	
			
			
	class Meta:
		verbose_name_plural="Metafields"
		verbose_name = "Metafield"
		ordering = ["source", "name"]
		
	def __unicode__(self):
		return "Metafield %d: %s" % (self.id, self.name)
	


