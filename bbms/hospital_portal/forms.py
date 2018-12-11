from django import forms
from .models import *

Blood_group=[
    ('O+','O-Positive'),
    ('O-','O-Negative'),
    ('A+','A-Positive'),
    ('A-','A-Negative'),
    ('B+','B-Positive'),
    ('B-','B-Negative'),
    ('AB+','AB-Positive'),
    ('AB-','AB-Negative'),
]
choices= [
    ('Red Blood Cells','RBCL'),
    ('Plasma','Plasma'),
    ('Platelets','Platelet'),
]
class Hospital_Form(forms.ModelForm):
    class Meta:
        model = Hospital_DataBase
        fields = ['blood_units', 'blood_group', 'blood_component']

    blood_units = forms.IntegerField()
    blood_group = forms.CharField(
        label='Blood Group: ',
        widget=forms.Select(
            choices=Blood_group,
        ),
    )
    blood_component = forms.CharField(
        label='Component Required: ',
        widget=forms.Select(
            choices=choices,
        ),
    )
