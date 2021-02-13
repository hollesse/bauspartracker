from django.contrib import admin

from bauspartrackerapp.models import Bausparvertrag, Sparbeitrag, Buchung

admin.site.register(Bausparvertrag, )
admin.site.register(Sparbeitrag)
admin.site.register(Buchung)
