from django.test import TestCase

from accounts.forms import loginform


class Test_Him(TestCase):
    def test_login_pass(self):
        form = loginform(data={"Who_are_you":"donor","username":"Kumar","password":"vijendra@123"})
        self.assertTrue(form.is_valid())

    def test_login_fail(self):
        form = loginform(data={"Who_are_you":"Kumar","username":"Saini","password":"vijendra@123"})
        self.assertFalse(form.is_valid())

    def test_attribute(self):
        form = loginform(data={"first_name":"Kumar","last_name":"Saini","email":"vijendra.cute@gmail.com"})
        self.assertTrue(form.fields['username'].label == 'Your User Name')
