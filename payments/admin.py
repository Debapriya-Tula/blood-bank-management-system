from django.contrib import admin
from .models import *

@admin.register(patientDetail, hospitalDetail, Diseases, donorDetail, Transaction)
class ViewAdmin(admin.ModelAdmin):
	pass
