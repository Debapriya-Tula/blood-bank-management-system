from django.db import models
from accounts.models import Patient_reg
from PIL import Image
# Create your models here.

class DataBase(models.Model):
	user_name = models.ForeignKey(Patient_reg, on_delete=models.PROTECT)
	picture = models.ImageField(default='default.jpg',upload_to = 'images/')
	blood_units = models.IntegerField(default='0')
	blood_group = models.CharField(max_length=11)
	to_time = models.TimeField(null=True, blank=True)
	from_time = models.TimeField(null=True, blank=True)
	order_complete = models.BooleanField(default=False)
	auth_complete = models.BooleanField(default=False)