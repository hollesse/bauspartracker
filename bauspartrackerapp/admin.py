from django.contrib import admin

from bauspartrackerapp.models import Bausparvertrag, Sparbeitrag, Buchung, SparbeitragJob

admin.site.register(Bausparvertrag)
admin.site.register(Sparbeitrag)
admin.site.register(Buchung)
admin.site.register(SparbeitragJob)
