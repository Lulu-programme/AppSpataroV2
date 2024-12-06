from django.contrib import admin
from .models import Factory, Station
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Factory, ImportExportModelAdmin)
admin.site.register(Station, ImportExportModelAdmin)
