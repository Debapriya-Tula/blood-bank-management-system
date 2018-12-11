from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class RBCL(models.Model):
	blood_type = models.CharField(max_length=100, choices=(
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
	donate_date=models.DateTimeField(default=timezone.now)
	time_left = models.FloatField(default=1010)
	expiry = models.IntegerField(default=1010)
	available = models.BooleanField(default=True)
	def __str__(self):
		return "Blood Type : {0} Units : {1} Date : {2}".format(self.blood_type, self.units, self.donate_date)


class Plasma(models.Model):
	blood_type = models.CharField(max_length=100, choices=(
													('O','O'),
													('A','A'),
													('B','B'),
													('AB','AB')
													),blank=False)
	units=models.IntegerField(default=0)
	donate_date=models.DateTimeField(default=timezone.now)
	time_left = models.FloatField(default=100)
	expiry = models.IntegerField(default=100)
	available = models.BooleanField(default=True)
	def __str__(self):
		return "Blood Type : {0} Units : {1} Date : {2}".format(self.blood_type, self.units, self.donate_date)


class Platelet(models.Model):
	units=models.IntegerField(default=0)
	donate_date=models.DateTimeField(default=timezone.now)
	time_left = models.FloatField(default=120)
	expiry = models.IntegerField(default=120)
	available = models.BooleanField(default=True)
	def __str__(self):
		return "Units : {0} Date : {1}".format(self.units, self.donate_date)


class frozen_cryo(models.Model):
	blood_type = models.CharField(max_length=100, choices=(
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
	donate_date=models.DateTimeField(default=timezone.now)
	time_left = models.FloatField(default=0)
	available = models.BooleanField(default=True)
	def __str__(self):
		return "Blood Type : {0} Units : {1} Date : {2}".format(self.blood_type, self.units, self.donate_date)


class RBCLs(models.Model):
	blood_type = models.CharField(max_length=100, choices=(
													('A+','A Positive'),
													('A-','A Negative'),
													('B+','B Positive'),
													('B-','B Negative'),
													('O+','O Positive'),
													('O-','O Negative'),
													('AB+','AB Positive'),
													('AB-','AB Negative'),
													), blank=False)
	price = models.IntegerField()
	current_inv = models.IntegerField(default=0)
	def __str__(self):
		return "Blood Type : {0} Price : {1} Current Inventory : {2}".format(self.blood_type, self.price, self.current_inv)

class Plasmas(models.Model):
	blood_type = models.CharField(max_length=100, choices=(
													('O','O'),
													('A','A'),
													('B','B'),
													('AB','AB')
													),blank=False)
	price = models.IntegerField()
	current_inv = models.IntegerField(default=0)

	def __str__(self):
		return "Blood Type : {0} Price : {1} Current Inventory : {2}".format(self.blood_type, self.price, self.current_inv)

class Platelets(models.Model):
	price = models.IntegerField()
	current_inv = models.IntegerField(default=0)

	def __str__(self):
		return "Price : {0} Current Inventory : {1}".format(self.price, self.current_inv)


class Frozen_Cryos(models.Model):
	blood_type = models.CharField(max_length=100, choices=(
													('A+','A Positive'),
													('A-','A Negative'),
													('B+','B Positive'),
													('B-','B Negative'),
													('O+','O Positive'),
													('O-','O Negative'),
													('AB+','AB Positive'),
													('AB-','AB Negative'),
													),blank=False)
	current_inv = models.IntegerField(default=0)

	def __str__(self):
		return "Blood Type : {0} Current Inventory : {1}".format(self.blood_type, self.current_inv)
