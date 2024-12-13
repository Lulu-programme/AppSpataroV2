from django.contrib import admin
from .models import StartDaytime, FactoryDaytime, GasoilDaytime, ChangeDaytime
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(StartDaytime, ImportExportModelAdmin)
admin.site.register(FactoryDaytime, ImportExportModelAdmin)
admin.site.register(GasoilDaytime, ImportExportModelAdmin)
admin.site.register(ChangeDaytime, ImportExportModelAdmin)
