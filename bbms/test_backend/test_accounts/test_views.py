from django.test import TestCase

from django.urls import reverse
from accounts import models
from InventoryManagement import models

class Test_Teller(TestCase):

    def test_view_url_exists_at_desired_location_pass(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_fail(self):
        response = self.client.get('/accounts/forgot_pass/')
        self.assertEqual(response.status_code, 200)


    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('accounts:confirm_register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/InventoryManagement/display_RBCL/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'InventoryManagement/index.html')
