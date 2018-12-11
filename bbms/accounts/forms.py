from django import forms

class loginform(forms.Form):
    CHOICES=[('donor','Donor'),
        ('hospital','Hospital'),
        ('user','Patient')]
    Who_are_you  = forms.ChoiceField(choices=CHOICES)
    username = forms.CharField(label='Your User Name', max_length=100)
    password = forms.CharField(label='Your Password', max_length=100, widget=forms.PasswordInput())

    
class passconfrm(forms.Form):
    password = forms.CharField(label='New Password', max_length=100, widget=forms.PasswordInput())
    passwordconfrm = forms.CharField(label='Confirm new Password', max_length=100, widget=forms.PasswordInput())