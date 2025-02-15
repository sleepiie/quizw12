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
