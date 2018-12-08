from django.db import models

# Create your models here.
class api_keys(models.Model):
	email = models.EmailField()
	api_key = models.CharField(max_length = 50)