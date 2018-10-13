from django.db import models

# Create your models here.

class Register(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    user_name = models.CharField(max_length = 100,unique = True)
    email = models.EmailField(max_length = 200,unique = True)
    password = models.CharField(max_length = 20)
    blood_group = models.CharField(max_length = 3)

    def __str__(self):
        return self.user_name
