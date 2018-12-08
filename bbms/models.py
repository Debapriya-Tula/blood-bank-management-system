from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator,MinLengthValidator


class Patient_reg(models.Model):
	#user = models.OneToOneField(User,on_delete = models.CASCADE)

	username = models.CharField(max_length = 50,blank =False)
	email = models.EmailField()
	password = models.CharField(max_length = 30)
	first_name = models.CharField(max_length = 30)
	las_name = models.CharField(max_length = 30)

	def __str__(self):
		return self.user.username

class Donor_reg(models.Model):
	
	username = models.CharField(max_length = 50,blank =False)
	email = models.EmailField()
	password = models.CharField(max_length = 30)
	first_name = models.CharField(max_length = 30)
	las_name = models.CharField(max_length = 30
	#user = models.OneToOneField(User,on_delete = models.CASCADE)

	# Addtional Fields
	city = models.CharField(max_length = 50)
	pincode = models.CharField(max_length = 6,validators=[MinLengthValidator(6)])
	state = models.CharField(max_length = 20)

	def __str__(self):
		return self.user.username


class Hospital_reg(models.Model):
	username = models.CharField(max_length = 50,blank =False)
	email = models.EmailField()
	password = models.CharField(max_length = 30)
	hospital_name = models.CharField(max_length = 100)
	ad_line1 = 
	city = models.CharField(max_length = 50)
	pincode = models.CharField(max_length = 6,validators=[MinLengthValidator(6)])
	state = models.CharField(max_length = 20)
	license = models.CharField(max_length = 10,validators=[MinLengthValidator(10)])
	#We verify the license later in the blood bank counter

	def __str__(self):
		return self.user.username


blood_grp_choices = (
					('O_pos','O+'),
					('O_neg','O-'),
					('A_pos','A+'),
					('A_neg','A-'),
					('B_pos','B+'),
					('B_neg','B-'),
					('AB_pos','AB+'),
					('AB_neg','AB-'),
)

class Patient_details(models.Model):
	user = models.ForeignKey(Patient_reg,on_delete = models.CASCADE)
	gender = models.CharField(max_length = 1, choices = (('M','Male'),('F','Female')))
	weight = models.IntegerField()
	height = models.IntegerField()
	blood_group = models.CharField(max_length = 3,choices = blood_grp_choices)
	d_o_b = models.DateField()
	''' Here also apply the same validation for the below two fields'''
	ph_no = models.CharField(validators=[MinLengthValidator(10)],max_length = 12)
	#Image field for certificate image verification
	#certification_no = models.CharField(validators=[MinLengthValidator(10)],max_length = 10)


class Donor_details(models.Model):
	user = models.ForeignKey(Donor_reg,on_delete = models.CASCADE)
	gender = models.CharField(max_length = 1,validators=[MinLengthValidator(1)])
	''' Has to be less than 100kgs'''
	weight = models.IntegerField()
	height = models.IntegerField()
	blood_group = models.CharField(max_length = 3,choices = blood_grp_choices)
	d_o_b = models.DateField()
	ph_no = models.CharField(validators=[MinLengthValidator(10)],max_length = 12, )
	# Here you make the changes that u told me
	last_donated_month = models.CharField(max_length = 12)
	last_donated_year = models.CharField(max_length = 12)


#

''' We don't need this model. We will just ask the user if he ahs any of these diseases
class Diseases(models.Model):
	hepatitis = models.BooleanField(default = False)
	AIDS = models.BooleanField(default = False)
	cancer = models.BooleanField(default = False)
	kidney_disease = models.BooleanField(default = False)
	heart_disease = models.BooleanField(default = False)
'''

class Blood_Inventory(models.Model):
	blood_grp = models.CharField(max_length = 3,choices = blood_grp_choices)
	total_samples = models.IntegerField()

class Blood_Price(models.Model):
	blood_grp = models.ForeignKey(Blood_Inventory,on_delete = models.CASCADE)
	price_per_unit = models.FloatField()


class Hospital(models.Model):
	''' We will maintain a checkbox for allowing multiple selections'''
	blood_grps_reqd = models.CharField(max_length = 3)
	blood_grp_quantity = models.IntegerField()
