from django.contrib import admin

from .models import veremail, Patient_reg, Patient_details, Donor_reg, Donor_details, Hospital_reg


admin.site.register(veremail)
admin.site.register(Patient_details)
admin.site.register(Patient_reg)
admin.site.register(Hospital_reg)
admin.site.register(Donor_details)
admin.site.register(Donor_reg)
