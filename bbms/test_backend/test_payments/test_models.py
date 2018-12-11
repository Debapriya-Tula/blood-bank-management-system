from django.test import TestCase

from payments.models import patientDetail,Transaction,donorDetail
from accounts.models import Patient_reg

class Test_patientDetail(TestCase):
    @classmethod
    def setUp(cls):
        patient = Patient_reg.objects.create(username = "Kumar",
                              email = "vijendra.raj@gmail.com",
                              password = "Kumar@123",
                              first_name = "Vijendra",
                              last_name="Saini",
                              email_verified = 1)
        patientDetail.objects.create(username = patient,
                              blood_type = "A+",
                              units = "10",
                              order_complete = True)

    def get_absolute_url(self):
        return reverse('patient-detail',args = [str(self.id)])
    def test_patientDetail(self):
        author = patientDetail.objects.get(blood_type="A+")
        field_label = author._meta.get_field('prescription').verbose_name
        self.assertEquals(field_label, 'prescription')

    def test_get_absolute_url(self):
        author = patientDetail.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        #self.assertEquals(author.get_absolute_url(), '/home/debapriya/Music/bbms/payments/models/1')


class Test_Transaction(TestCase):
    @classmethod
    def setUp(cls):
        Transaction.objects.create(token = "23451a",
                              order_id = "cef23",
                              timestamp = 1,
                              amount = 234.56,
                              success = True)

    def test_func(self):
        author = Transaction.objects.get(token = "23451a")
        self.assertEquals(author.__str__(),"23451a")
