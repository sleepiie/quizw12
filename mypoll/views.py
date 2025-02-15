from django.shortcuts import render
from mypoll.models import Question , Choice
from django.utils import timezone

def home_page(request): 

    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    

    return render(request, "home.html" , {'latest_question_list':latest_question_list})
