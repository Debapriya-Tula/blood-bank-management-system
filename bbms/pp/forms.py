from django import forms
from .models import *

class Profile_Form(forms.ModelForm):
    class Meta:
        model = DataBase
        fields = ['picture', 'pic_name']