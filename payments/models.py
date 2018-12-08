from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from accounts.models import Donor_reg, Hospital_reg, Patient_reg


class patientDetail(models.Model):
	username = models.ForeignKey(Patient_reg, on_delete=models.CASCADE)
	blood_type=models.CharField(max_length=100, choices =(
													('A+','A Positive'),
													('A-','A Negative'),
													('B+','B Positive'),
													('B-','B Negative'),
													('O+','O Positive'),
													('O-','O Negative'),
													('AB+','AB Positive'),
													('AB-','AB Negative'),
													), blank=False)
	units=models.IntegerField(default=0)
	prescription = models.ImageField(default='payments/default.jpg', upload_to='payments/')
	order_complete = models.BooleanField(default=False)
	date_ordered = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return "User : {0} Blood Type : {1} Units : {2} Order Completed : {3}".format(self.username.username,self.blood_type, self.units, self.order_complete)

		def save(self):
			super().save()

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


class donorDetail(models.Model):
	username = models.ForeignKey(Donor_reg, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)
	donate_complete = models.BooleanField(default=False)

	def __str__(self):
		return "Date of Donation: {0} Donation Completed : {1} ".format(self.date, self.donate_complete)

		def save(self):
			super().save()

class Diseases(models.Model):
	donor = models.OneToOneField(donorDetail, on_delete=models.CASCADE)
	Asthma = models.BooleanField(default=False)
	Cancer = models.BooleanField(default=False)
	Cardiac_Disease = models.BooleanField(default=False)
	Diabetes = models.BooleanField(default=False)
	Hypertension = models.BooleanField(default=False) 
	Pyschiatric_Disorder = models.BooleanField(default=False)
	Epilepsy = models.BooleanField(default=False)

class hospitalDetail(models.Model):
	username = models.ForeignKey(Hospital_reg, on_delete=models.CASCADE)
	blood_type=models.CharField(max_length=100, choices =(
													('A+','A Positive'),
													('A-','A Negative'),
													('B+','B Positive'),
													('B-','B Negative'),
													('O+','O Positive'),
													('O-','O Negative'),
													('AB+','AB Positive'),
													('AB-','AB Negative'),
													), blank=False)
	units=models.IntegerField(default=0)
	component = models.CharField(max_length=100, choices=(
									('RBCLs','Red Blood Cells'),
									('Plasmas', 'Plasma'),
									('Platelets','Platelets'),
									),blank=True)
	order_complete = models.BooleanField(default=False)
	date_ordered = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return "User : {0} Blood Type : {1} Units : {2} Order Completed : {3}".format(self.username.username,self.blood_type, self.units, self.order_complete)
		
		def save(self):
			super().save()

class finalorder(models.Model):
	#order = models.OneToOneField(patientDetail, on_delete=models.CASCADE) 
	component = models.CharField(max_length=100, choices=(
									('RBCLs','Red Blood Cells'),
									('Plasmas', 'Plasma'),
									('Platelets','Platelets'),
									),blank=True)
	order_complete=models.BooleanField(default=False)
	def __str__(self):
		return self.component

