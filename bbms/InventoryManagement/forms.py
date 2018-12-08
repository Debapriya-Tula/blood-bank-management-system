from django import forms
from .models import *
from django.utils import timezone
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

class AddStock(forms.Form):
	units = forms.IntegerField(min_value=1, label='Number of Units')
	blood_type = forms.ChoiceField(choices=choices, label='Blood Type')

class DeleteStock(forms.Form):
	units = forms.IntegerField(min_value=1, label='Number of Units')
	blood_type = forms.ChoiceField(choices=choices, label='Blood Type')
	component = forms.ChoiceField(choices=ch, label='Component Required')


