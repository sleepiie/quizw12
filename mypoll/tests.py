# tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from mypoll.models import Question, Choice
from django.utils import timezone

class VoteViewTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="วันนี้อากาศเป็นยังไงบ้าง", 
            pub_date=timezone.now()
        )
        self.choice_good = Choice.objects.create(
            question=self.question, choice_text="อากาศดี", votes=0
        )
        self.choice_rain = Choice.objects.create(
            question=self.question, choice_text="คิดว่าฝนจะตก", votes=0
        )
        self.choice_hot = Choice.objects.create(
            question=self.question, choice_text="อากาศร้อนเกินไป", votes=0
        )
        self.choice_cold = Choice.objects.create(
            question=self.question, choice_text="อากาศหนาว", votes=0
        )
    
    def test_vote_success(self):
        response = self.client.post(
            reverse("mypoll:vote", args=[self.question.id]),
            {"choice": self.choice_good.id}
        )
        self.assertEqual(response.status_code, 302)
        self.choice_good.refresh_from_db()
        self.assertEqual(self.choice_good.votes, 1)
    
    
    def test_vote_no_selection(self):
        response = self.client.post(
            reverse("mypoll:vote", args=[self.question.id]),
            {}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "คุณยังไม่ได้เลือกตัวเลือกใดๆ")

class RatingTest(TestCase):
    def setUp(self):
        
        self.question1 = Question.objects.create(
            question_text="วันนี้อากาศเป็นยังไงบ้าง", 
            pub_date=timezone.now()
        )
        Choice.objects.create(question=self.question1, choice_text="อากาศดี", votes=10)
        Choice.objects.create(question=self.question1, choice_text="คิดว่าฝนจะตก", votes=2)
        Choice.objects.create(question=self.question1, choice_text="อากาศร้อนเกินไป", votes=5)
        Choice.objects.create(question=self.question1, choice_text="อากาศหนาว", votes=0)
        
        self.question2 = Question.objects.create(
            question_text="เย็นนี้กินอะไรดี", 
            pub_date=timezone.now()
        )
        Choice.objects.create(question=self.question2, choice_text="ผัดไท", votes=10)
        Choice.objects.create(question=self.question2, choice_text="แกงเขียวหวาน", votes=20)
        Choice.objects.create(question=self.question2, choice_text="หมูกรอบ", votes=30)
        Choice.objects.create(question=self.question2, choice_text="ไข่เจียว", votes=5)

    def testrating(self):
        response = self.client.get(reverse('mypoll:homepage'))
        self.assertContains(response, '!!Hot')
        self.assertContains(response, '!Warm')

class PrivatePollTest(TestCase):
    def setUp(self):
        self.question1 = Question.objects.create(
            question_text="ใช้การ์ดจอค่ายไหน", 
            pub_date=timezone.now(),
            is_private = True
        )
        Choice.objects.create(question=self.question1, choice_text="Nvidia", votes=30)
        Choice.objects.create(question=self.question1, choice_text="Amd", votes=20)
        Choice.objects.create(question=self.question1, choice_text="Intel", votes=10)
    def test_private_page(self):
        response = self.client.get(reverse('mypoll:private_poll'))
        self.assertContains(response, 'ใช้การ์ดจอค่ายไหน - !!Hot')
        self.assertContains(response, 'Nvidia')
        self.assertContains(response, 'Amd')
        self.assertContains(response, 'Intel')

class OnlyPollTest(TestCase):
    def setUp(self):
        self.question1 = Question.objects.create(
            question_text="ใช้การ์ดจอค่ายไหน", 
            pub_date=timezone.now(),
            is_private = True
        )
        Choice.objects.create(question=self.question1, choice_text="Nvidia", votes=30)
        Choice.objects.create(question=self.question1, choice_text="Amd", votes=20)
        Choice.objects.create(question=self.question1, choice_text="Intel", votes=10)

        self.question2 = Question.objects.create(
            question_text="ใช้ cpu ค่ายไหน", 
            pub_date=timezone.now(),
            is_private = True
        )
        Choice.objects.create(question=self.question2, choice_text="Intel", votes=10)
        Choice.objects.create(question=self.question2, choice_text="Amd", votes=0)

    def test_only_you_poll_page(self):
        response = self.client.get(reverse('mypoll:onlypoll' , args=[self.question2.id]))
        self.assertContains(response, 'Only you poll')
        self.assertContains(response, 'ใช้ cpu ค่ายไหน')
        self.assertContains(response, 'Amd')
        self.assertContains(response, 'Intel')