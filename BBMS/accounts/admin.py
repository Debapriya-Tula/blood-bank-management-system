from django.contrib import admin

from .models import veremail, Patient_reg, Patient_details, Donor_reg, Donor_details, Hospital_reg

#Register your models here

class Patient_regAdmin(admin.ModelAdmin):
    fields = ['username','email','first_name','last_name','email_verified']
    search_fields = ['username','email','first_name']

    list_filter = ['username','email_verified']
    list_display = ['username','email','first_name','last_name','email_verified']


class Donor_regAdmin(admin.ModelAdmin):
    fields = ['username','email','first_name','las_name','email_verified']
    search_fields = ['username','email','first_name']

    list_filter = ['username','email_verified']
    list_display = ['username','email','first_name','las_name','email_verified']


class Patient_detailsAdmin(admin.ModelAdmin):
    fields = ['userp','gender','blood_group','d_o_b','ph_no']
    search_fields = ['userp','blood_group','d_o_b']

    list_filter = ['userp','gender','blood_group']
    list_display = ['userp','blood_group','gender','d_o_b','ph_no']


class Donor_detailsAdmin(admin.ModelAdmin):
    fields = ['userd','ad_line1','ad_line2','city','pincode','state','gender','weight','height','blood_group','d_o_b','ph_no']
    search_fields = ['userd','blood_group','d_o_b','city','state']

    list_filter = ['userd','gender','blood_group','city','state']
    list_display = ['userd','blood_group','gender','d_o_b','ph_no']


class Hospital_regAdmin(admin.ModelAdmin):
    fields = ['username','email','hospital_name','ad_line1','ad_line2','city','pincode','state','license']
    search_fields = ['username','email','hospital_name','city']

    list_filter = ['username','hospital_name','city']
    list_display = ['username','email','hospital_name','ad_line1','city','pincode','state','license']



admin.site.register(veremail)
admin.site.register(Patient_reg,Patient_regAdmin)
admin.site.register(Patient_details,Patient_detailsAdmin)
admin.site.register(Donor_reg,Donor_regAdmin)
admin.site.register(Donor_details,Donor_detailsAdmin)
admin.site.register(Hospital_reg,Hospital_regAdmin)
#admin.site.register(m.Hospital_reg,Donor_detailsAdmin)
    
    
    
