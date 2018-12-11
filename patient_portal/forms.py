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
class Profile_Form(forms.ModelForm):
    class Meta:
        model = DataBase
        fields = ['picture', 'blood_units']

    blood_group = forms.CharField(
        label='Blood Group: ',
        widget=forms.Select(
            choices=Blood_group,
            attrs={
                'id': 'blood_grp',
            }
        ),
    )
    to_time=forms.TimeField(
        required=True,
        widget=forms.TimeInput(
            attrs={
                'type': 'time'
            }
        )
    )
    from_time=forms.TimeField(
        required=True,
        widget=forms.TimeInput(
            attrs={
                'type': 'time'
            }
        )
    )
