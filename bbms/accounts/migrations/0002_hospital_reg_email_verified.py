# Generated by Django 2.1 on 2018-12-01 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital_reg',
            name='email_verified',
            field=models.IntegerField(null=True),
        ),
    ]