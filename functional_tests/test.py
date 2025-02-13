from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

class usertest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_homepage(self):
        self.browser.get("http://localhost:8000")
        self.assertIn("mypoll" , self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text 
        self.assertIn("My Poll", header_text)

        time.sleep(2)