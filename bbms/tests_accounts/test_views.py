'''
from django.test import TestCase

from notify.views import tell_admin
from django.urls import reverse

class Test_Teller(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_requests = 5
        
        for req in range(number_of_requests):
            Author.objects.create(
                first_name=f'Christian {req}',
                last_name=f'Surname {req}',
            )
        

    def test_view_url_exists_at_desired_location_pass(self):
        response = self.client.get('/notify/tell_admin/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_fail(self):
        response = self.client.get('/notify/tell_admin/')
        self.assertEqual(response.status_code, 200)


    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('notify:tell_admin'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('notify:tell_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notify/form.html')
'''