from django import forms
from .models import *
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

class admin_fillform(forms.ModelForm):
	class Meta:
		model = finalorder
		fields = ['component']

class admin_donorform(forms.ModelForm):
	class Meta:
		model = finaldonation
		fields = ['units']