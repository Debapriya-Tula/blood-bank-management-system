# Generated by Django 2.1.3 on 2018-11-17 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic_name', models.CharField(max_length=50)),
                ('picture', models.ImageField(upload_to='images')),
            ],
        ),
    ]