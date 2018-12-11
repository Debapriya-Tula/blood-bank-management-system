from django.test import TestCase

from accounts.models import Patient_reg,Patient_details

class Test_Patient_reg(TestCase):
    @classmethod
    def setUp(cls):
        Patient_reg.objects.create(username = "Kumar",
                              email = "vijendra.raj@gmail.com",
                              password = "Kumar@123",
                              first_name = "Vijendra",
                              last_name="Saini",
                              email_verified = 1)

    def test_first_name_label(self):
        author = Patient_reg.objects.get(first_name="Vijendra")
        field_label = author._meta.get_field('email').verbose_name
        self.assertEquals(field_label, "email")

    def test_func(self):
        author = Patient_reg.objects.get(last_name="Saini")
        self.assertEquals(author.__str__(),'Kumar')



class Test_Donor_details(TestCase):
    @classmethod
    def setUp(cls):
        patient = Patient_reg.objects.create(username = "Kumar",
                              email = "vijendra.raj@gmail.com",
                              password = "Kumar@123",
                              first_name = "Vijendra",
                              last_name="Saini",
                              email_verified = 1)
        Patient_details.objects.create(userp = patient,gender = "M",blood_group = "AB+",d_o_b="1998-12-30",ph_no = "1234567891012")
        
    def test_gender(self):
        author = Patient_details.objects.get(userp__first_name="Vijendra")
        field_label = author._meta.get_field('gender').verbose_name
        self.assertEquals(field_label, "gender")
