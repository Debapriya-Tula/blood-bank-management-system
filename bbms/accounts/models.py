from django.db import models

class veremail(models.Model):
	ab = models.IntegerField()
	uname = models.CharField(max_length=50)

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
gender_choices = (
					('Male','M'),
					('Female','F'),
					('Other','T'),
)

class Patient_reg(models.Model):
	username = models.CharField(max_length = 50,blank =False)
	email = models.EmailField()
	password = models.CharField(max_length = 30)
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30)
	email_verified = models.IntegerField(null=True)

	def __str__(self):
		return self.username

class Patient_details(models.Model):
	userp = models.ForeignKey(Patient_reg,on_delete = models.CASCADE)
	gender = models.CharField(max_length = 1, choices = gender_choices)
#	weight = models.IntegerField()
#	height = models.IntegerField()
	blood_group = models.CharField(max_length = 3,choices = blood_grp_choices)
	d_o_b = models.DateField()
	ph_no = models.CharField(max_length = 12)

class Donor_reg(models.Model):
	username = models.CharField(max_length = 50,blank =False)
	email = models.EmailField()
	password = models.CharField(max_length = 30)
	first_name = models.CharField(max_length = 30)
	las_name = models.CharField(max_length = 30)
	email_verified = models.IntegerField(null=True)

	def __str__(self):
		return self.username

class Donor_details(models.Model):
	userd = models.ForeignKey(Donor_reg,on_delete = models.CASCADE)
	ad_line1 = models.CharField(max_length=150)
	ad_line2 = models.CharField(max_length=150)
	city = models.CharField(max_length = 50)
	pincode = models.CharField(max_length = 6)
	state = models.CharField(max_length = 20)
	gender = models.CharField(max_length = 1,choices = gender_choices)
	weight = models.IntegerField()
	height = models.IntegerField()
	blood_group = models.CharField(max_length = 3,choices = blood_grp_choices)
	d_o_b = models.DateField()
	ph_no = models.CharField(max_length = 12 )

class Hospital_reg(models.Model):
	username = models.CharField(max_length = 50,blank =False)
	email = models.EmailField()
	password = models.CharField(max_length = 30)
	hospital_name = models.CharField(max_length = 100)
	ad_line1 = models.CharField(max_length=150)
	ad_line2 = models.CharField(max_length=150)
	city = models.CharField(max_length = 50)
	pincode = models.CharField(max_length = 6)
	state = models.CharField(max_length = 20)
	license = models.CharField(max_length = 10)
	email_verified = models.IntegerField(null=True)

#	ph_no = models.IntegerField()

	def __str__(self):
		return self.username