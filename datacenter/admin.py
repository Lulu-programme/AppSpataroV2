from django.contrib import admin
from .models import Working, Product
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Working, ImportExportModelAdmin)
admin.site.register(Product, ImportExportModelAdmin)
