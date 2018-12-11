'''
from django.test import TestCase

from notify.forms import Person_form


class Test_Him(TestCase):
    def test_person_pass(self):
        form = Person_form(data={"first_name":"Kumar","last_name":"Saini","email":"vijendra.cute@gmail.com"})
        self.assertTrue(form.is_valid())

    def test_person_fail(self):
        form = Person_form(data={"first_name":"Vij","last_name":"Saini","email":"vijendra.cutegmail.com"})
        self.assertFalse(form.is_valid())

    def test_attribute(self):
        form = Person_form(data={"first_name":"Kumar","last_name":"Saini","email":"vijendra.cute@gmail.com"})
        self.assertTrue(form.fields["first_name"]=="first name")


'''
