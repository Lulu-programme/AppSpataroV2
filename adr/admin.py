from django.contrib import admin
from .models import Adr
from import_export.admin import ImportExportModelAdmin


admin.site.register(Adr, ImportExportModelAdmin)
