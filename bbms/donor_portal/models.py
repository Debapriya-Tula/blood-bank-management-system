from django.db import models
from accounts.models import Donor_reg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))


class Donor_DataBase(models.Model):
    user_name = models.ForeignKey(Donor_reg, on_delete=models.PROTECT)       					
    don_or_sell = models.CharField(max_length=10) 
    #diseases = models.CharField(max_length=80)
    #to_time = models.TimeField()
    last_donate_date = models.DateTimeField(default=timezone.now)
    #from_time = models.TimeField()
    donation_complete = models.BooleanField(default = False)

class Diseases(models.Model):
	donor = models.OneToOneField(Donor_DataBase, on_delete=models.CASCADE)
	Asthma = models.CharField(max_length=3, default='No')
	Cancer = models.CharField(max_length=3, default='No')
	Cardiac_Disease = models.CharField(max_length=3, default='No')
	Diabetes = models.CharField(max_length=3, default='No')
	Hypertension = models.CharField(max_length=3, default='No') 
	Kidney_Disease = models.CharField(max_length=3, default='No')
	Epilepsy = models.CharField(max_length=3, default='No')
	HIV = models.CharField(max_length=3, default='No')

