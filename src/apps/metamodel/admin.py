from django.contrib import admin
from .models import *


admin.site.register(Metafield, Metafield.Admin)
admin.site.register(Implementation, Implementation.Admin)
