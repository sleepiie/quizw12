from django.shortcuts import get_object_or_404, render, redirect
from mypoll.models import Question , Choice
from django.utils import timezone

def home_page(request): 
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now(),is_private=False).order_by("-pub_date")[:5]

    question_rating = []

    for question in latest_question_list:
        total_votes = 0
        choices = question.choice_set.all()
        for choice in choices:
            total_votes += choice.votes

        if total_votes >= 50:
            rating = "!!Hot"
        elif total_votes >= 10:
            rating = "!Warm"
        else:
            rating = ""
                
        question.rating = rating
        question_rating.append(question)

    return render(request, "home.html" , {'latest_question_list':question_rating})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'home.html', {
            'latest_question_list': [question],
            'error_message': "คุณยังไม่ได้เลือกตัวเลือกใดๆ",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('mypoll:results', question_id=question.id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})


def private_poll(request):
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now(),is_private=True).order_by("-pub_date")[:5]

    question_rating = []

    for question in latest_question_list:
        total_votes = 0
        choices = question.choice_set.all()
        for choice in choices:
            total_votes += choice.votes

        if total_votes >= 50:
            rating = "!!Hot"
        elif total_votes >= 10:
            rating = "!Warm"
        else:
            rating = ""
                
        question.rating = rating
        question_rating.append(question)

    return render(request, "private_poll.html" , {'latest_question_list':question_rating})


def onlypoll(request,question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    if question.is_private == False:
        return redirect('/')
    return render(request, 'onlypoll.html', {'question': question})