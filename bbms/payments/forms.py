from django import forms
from .models import *
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

    
'''class Inventory(forms.ModelForm):
	class Meta:
		model = Inventory
		fields = ('blood_type', , )'''

choices=(('A+','A Positive'),
		('A-','A Negative'),
		('B+','B Positive'),
		('B-','B Negative'),
		('O+','O Positive'),
		('O-','O Negative'),
		('AB+','AB Positive'),
		('AB-','AB Negative'),
		)
ch=(('RBCL','Red Blood Cells'),
	('Plasma','Plasma'),
	('Platelet','Platelets'),
	)
class blood_buyform(forms.ModelForm):
	#prescription=forms.ImageField()
	class Meta:
		model = patientDetail
		fields = ['blood_type', 'units', 'prescription']

class admin_fillform(forms.ModelForm):
	class Meta:
		model = finalorder
		fields = ['component']

class blood_donateform(forms.Form):
	date = forms.DateField(widget = forms.SelectDateWidget(), label="When do you want to donate?")

class disease(forms.ModelForm):
	'''def __init__(self):
				 	if check_something():
						self.fields['Asthma'].initial = False
						self.fields['Cancer'].initial = False
						self.fields['Cardiac_Disease'].initial = False
						self.fields['Diabetes'].initial = False
						self.fields['Hypertension'].initial = False
						self.fields['Epilepsy'].initial = False'''
	Asthma = forms.BooleanField()
	Cancer = forms.BooleanField()
	Cardiac_Disease = forms.BooleanField()
	Diabetes = forms.BooleanField()
	Hypertension = forms.BooleanField()
	Psychiatric_Disorder = forms.BooleanField()
	Epilepsy = forms.BooleanField()

	class Meta:
		model = Diseases
		fields = ['Asthma','Cancer','Cardiac_Disease','Diabetes','Psychiatric_Disorder','Epilepsy']
		

class blood_hospitalform(forms.ModelForm):
	class Meta:
		model = hospitalDetail
		fields = ['blood_type', 'units', 'component']

'''class blood_cartform(forms.Form):
	blood_type = forms.ChoiceField(choices=choices, label='Which Blood Type do you require?')
	units = forms.IntegerField(min_value=1, label='How many number of units do you need?')
	address = forms.CharField(required=True, label='Address')
	Prescription = forms.ImageField()
	'''




