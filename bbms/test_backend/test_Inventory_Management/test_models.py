from django.test import TestCase

from InventoryManagement.models import RBCL,Plasmas,frozen_cryo

class Test_RBCL(TestCase):
    @classmethod
    def setUp(cls):
        RBCL.objects.create(blood_type = "A+",
                              units = "10")

    def test_RBCL(self):
        author = RBCL.objects.get(blood_type="A+")
        field_label = author._meta.get_field('time_left').verbose_name
        self.assertEquals(field_label, "time left")

    def test_func(self):
        author = RBCL.objects.get(units=10)
        self.assertEquals(author.__str__(),"Blood Type : AB+ Units : 10 Date : 2018-12-11")


class Test_Plasmas(TestCase):
    @classmethod
    def setUp(cls):
        Plasmas.objects.create(blood_type = "O+",
                              price = "500",
                              current_inv = 1)

    def test_Plasmas(self):
        author = Plasmas.objects.get(blood_type="O+")
        field_label = author._meta.get_field('current_inv').verbose_name
        self.assertEquals(field_label, "current inv")
