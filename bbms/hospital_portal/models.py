from django.db import models
from accounts.models import Hospital_reg	
class Hospital_DataBase(models.Model):
	hosp_id = models.ForeignKey(Hospital_reg, on_delete=models.PROTECT)
	blood_units = models.IntegerField(default=0)
	blood_group = models.CharField(max_length=11)
	blood_component = models.CharField(max_length=100, default='RBCL')
	order_complete = models.BooleanField(default = False)