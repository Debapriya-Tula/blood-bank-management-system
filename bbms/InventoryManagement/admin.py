from django.contrib import admin
from .models import *

@admin.register(RBCL, Plasma, Platelet, frozen_cryo, RBCLs, Plasmas, Platelets, Frozen_Cryos)
class ViewAdmin(admin.ModelAdmin):
	pass
