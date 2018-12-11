from django import forms
from patient_portal import forms as patient_forms
from .models import *

CHOICES = patient_forms.Blood_group

radio_button=[
    ('donate','donate'),
    ('sell','sell'),
]
disease_radio=[
    ('Yes','Yes'),
    ('No','No'),
]


class Donor_Form(forms.ModelForm):
    class Meta:
        model = Donor_DataBase
        fields = ['don_or_sell','last_donate_date']

    #last_donate_date = forms.DateTimeField()
    don_or_sell = forms.CharField(
        widget = forms.RadioSelect(
            choices = radio_button,

        )
    )

       
class Disease_form(forms.ModelForm):
    class Meta:
        model = Diseases


        fields = ['Asthma', 'Cancer', 'Cardiac_Disease', 'Diabetes', 'Epilepsy', 'Hypertension', 'Kidney_Disease', 'HIV']
    Asthma = forms.CharField(
    widget = forms.RadioSelect(
        choices = disease_radio,

        )
    )
    Cancer = forms.CharField(
        widget = forms.RadioSelect(
            choices = disease_radio,

        )
    )
    Cardiac_Disease = forms.CharField(
        widget = forms.RadioSelect(
            choices = disease_radio,

        )
    )
    Diabetes = forms.CharField(
        widget = forms.RadioSelect(
            choices = disease_radio,

        )
    )
    Epilepsy = forms.CharField(
        widget = forms.RadioSelect(
            choices = disease_radio,

        )
    )
    Hypertension = forms.CharField(
        widget = forms.RadioSelect(
            choices = disease_radio,

        )
    )
    Kidney_Disease = forms.CharField(
        widget = forms.RadioSelect(
            choices = disease_radio,

        )
    )
    HIV = forms.CharField(
        widget = forms.RadioSelect(
            choices = disease_radio,

        )
    )

