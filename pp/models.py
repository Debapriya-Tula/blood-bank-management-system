from django.db import models

# Create your models here.
class DataBase(models.Model):
    pic_name = models.CharField(max_length=50, blank=True)
    picture = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.pic_name
