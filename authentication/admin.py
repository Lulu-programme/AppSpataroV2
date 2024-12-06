from django.contrib import admin
from .models import Account, Truck
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Account, ImportExportModelAdmin)
admin.site.register(Truck, ImportExportModelAdmin)
