from django.contrib import admin
from .models import PO,Vendor,Performance


admin.site.register(Vendor)
admin.site.register(PO)
admin.site.register(Performance)
