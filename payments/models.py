from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from accounts.models import Donor_reg, Hospital_reg, Patient_reg
from patient_portal.models import *
from donor_portal.models import *
from hospital_portal.models import *


class Transaction(models.Model):
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']

class finalorder(models.Model):
	order = models.OneToOneField(DataBase, on_delete=models.CASCADE)
	component = models.CharField(max_length=100, choices=(
									('RBCLs','Red Blood Cells'),
									('Plasmas', 'Plasma'),
									('Platelets','Platelets'),
									),blank=True)
	order_complete=models.BooleanField(default=False)
	def __str__(self):
		return "User : {0} Number of Units : {1} Blood Type : {2} Component : {3} Order Complete : {4}".format(self.order.user_name.username, self.order.blood_units, self.order.blood_group, self.component, self.order_complete)

class finaldonation(models.Model):
	donation = models.OneToOneField(Donor_DataBase, on_delete=models.CASCADE)
	units = models.CharField(max_length=2, choices=(
								('1','1'),
								('2','2'),
								),blank=True)
	def __str__(self):
		return "User : {0} Number of Units : {1} ".format(self.donation.user_name.username, self.units)
