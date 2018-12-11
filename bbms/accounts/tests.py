from django.test import TestCase
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import os
# Create your tests here.

class TestUserCreation(LiveServerTestCase):
    """
    class to test the user creation form
    """
    def setUp(self):
        self.selenium = webdriver.Chrome(os.path.dirname(os.path.abspath('chromedriver')+'/chromedriver'))
        super(TestUserCreation, self).setUp()


    def tearDown(self):
        self.selenium.quit()
        super(TestUserCreation, self).tearDown()


    def test_UserCreation(self):
        sel = self.selenium

        # Accessing the URL
        sel.get("https://127.0.0.1:8000/accounts/login")

        # WebDriverWait(self.selenium, 10).until(lambda selenium: self.selenium.find_element_by_id('id_username'))

        # Find the form elements
        frame = sel.find_element_by_xpath('//table[@name="main"]')
        sel.switch_to.frame(frame)
        user_name = sel.find_element_by_id('who0')
        #email = sel.find_element_by_id('id_email')
        #pass1 = sel.find_element_by_id('id_password1')
        #pass2 = sel.find_element_by_id('id_password2')
        #pin = sel.find_element_by_name('id_pincode')
        submit_btn = sel.find_element_by_class_name('buttonall')

        # Fill the form with data
        user_name.send_keys("Donor")
        #email.send_keys('sravanvinakota@gmail.com')
        #pass1.send_keys('hello')
        #pass2.send_keys('hello')
        #pin.send_keys(123446)

        # hit the submit button
        submit_btn.send_keys(Keys.RETURN)
