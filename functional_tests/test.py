from django.test import LiveServerTestCase
from selenium import webdriver
from django.urls import reverse
from django.utils import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from mypoll.models import Question, Choice


class usertest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_homepage(self):
        self.question = Question.objects.create(
            question_text="วันนี้อากาศเป็นยังไงบ้าง", 
            pub_date=timezone.now()
        )
        Choice.objects.create(question=self.question, choice_text="อากาศดี", votes=0)
        Choice.objects.create(question=self.question, choice_text="คิดว่าฝนจะตก", votes=0)
        Choice.objects.create(question=self.question, choice_text="อากาศร้อนเกินไป", votes=0)
        Choice.objects.create(question=self.question, choice_text="อากาศหนาว", votes=0)

        #แทนเจอเว็บหนึ่งเป็น เว็บแบบสำรวจ แทนเห็นว่าหน้าสนใจเลยลองกดเข้าไปดู
        self.browser.get(self.live_server_url)
        self.assertIn("mypoll" , self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text 
        self.assertIn("My Poll", header_text)

        #แทนเห็นคำถาม ถามว่าวันนี้อากาศเป็นยังไงบ้าง
        header = self.browser.find_element(By.TAG_NAME, "h2")   
        self.assertIn("วันนี้อากาศเป็นยังไงบ้าง", header.text)


        #แทนเห็นตัวเลือกสำหรับ vote 4 อันคือ "1.อากาศดี" "2.คิดว่าฝนจะตก" "3.อากาศร้อนเกินไป" "4.อากาศหนาว"
        expected_choices = ["อากาศดี", "คิดว่าฝนจะตก", "อากาศร้อนเกินไป", "อากาศหนาว"]
        labels = self.browser.find_elements(By.TAG_NAME, "label")
        found_choices = [label.text for label in labels]
        for choice_text in expected_choices:
            self.assertIn(choice_text, found_choices, f"ไม่พบตัวเลือก: {choice_text}")
        time.sleep(1)
        

        #แทนคิดว่าวันนี้อากาศดีจึงได้กด vote "1.อากาศดี" ไป
        choice_radio = self.browser.find_element(By.ID, "choice1")
        choice_radio.click()

        submit_button = self.browser.find_element(By.ID, "vote")
        submit_button.click()
        time.sleep(1)


        #หน้าเว็บถูกเปลี่ยนเป็นหน้าแสดงผล vote โดยจะแสดงผล vote ของแต่ละตัวเลือกและมี ปุ่มให้กดกลับไป vote อีกครั้ง
        result_header = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(result_header.text.strip(), "results")
        choices = self.browser.find_elements(By.TAG_NAME, "li")
        self.assertTrue(any("อากาศดี" in li.text and "1" in li.text for li in choices))
        time.sleep(1)

        #แทนลองกดปุ่มกลับไป vote อีกครั้ง หน้าเว็บพาแทนกลับไปยังหน้าคำถามเดิม
        back_link = self.browser.find_element(By.LINK_TEXT, "กลับไปหน้าหลัก")
        back_link.click()
       
        header = self.browser.find_element(By.TAG_NAME, "h2")
        self.assertIn("วันนี้อากาศเป็นยังไงบ้าง", header.text)

        time.sleep(1)