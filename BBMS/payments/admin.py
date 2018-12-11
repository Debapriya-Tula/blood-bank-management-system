from django.contrib import admin
from .models import *

@admin.register(finalorder, Transaction, finaldonation)
class ViewAdmin(admin.ModelAdmin):
	pass
