from django.db import models

class donors(models.Model):
#	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=150,null=True)
	email = models.CharField(max_length=50)
	uname = models.CharField(max_length=50)
	passwd = models.CharField(max_length=30)
	dob = models.DateField()
	line1 = models.CharField(max_length=150)
	line2 = models.CharField(max_length=150)
	postalcode = models.CharField(max_length=6)
	city = models.CharField(max_length=150)
	country = models.CharField(max_length=150)
	email_verified = models.IntegerField(max_length=1,null=True)

class hospital(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=150,null=True)
	email = models.CharField(max_length=50)
	uname = models.CharField(max_length=50)
	passwd = models.CharField(max_length=30)
	license = models.CharField(max_length=30)
	l_exp = models.DateField()
	line1 = models.CharField(max_length=150)
	line2 = models.CharField(max_length=150)
	postalcode = models.CharField(max_length=6)
	city = models.CharField(max_length=150)
	country = models.CharField(max_length=150)

class users(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=150,null=True)
	email = models.CharField(max_length=50)
	uname = models.CharField(max_length=50)
	passwd = models.CharField(max_length=30)
	dob = models.DateField()

class temp_db(models.Model):
	uname = models.CharField(max_length=50)
	code = models.IntegerField(max_length=6)