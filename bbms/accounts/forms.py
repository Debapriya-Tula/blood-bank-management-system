from django import forms

class loginform(forms.Form):
    CHOICES=[('donor','donor'),
        ('hospital','hospital'),
        ('user','user')]
    Who_are_you  = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    username = forms.CharField(label='Your User Name', max_length=100)
    password = forms.CharField(label='Your Password', max_length=100, widget=forms.PasswordInput())

    
class passconfrm(forms.Form):
    password = forms.CharField(label='New Password', max_length=100, widget=forms.PasswordInput())
    passwordconfrm = forms.CharField(label='Confirm new Password', max_length=100, widget=forms.PasswordInput())