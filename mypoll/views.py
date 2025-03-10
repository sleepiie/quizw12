from django.shortcuts import get_object_or_404, render, redirect
from mypoll.models import Question , Choice
from django.utils import timezone

def home_page(request): 
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

    choice_vote = 0
    ratings = []

    for i in range (1,len(latest_question_list)):
        question = Question.objects.get(id=i)
        for j in range (1,5):
            choice = question.choice_set.get(pk=j)
            choicevote=choice.votes
            choice_vote += choicevote
            if choice_vote >= 50:
                rating = "hot"
            elif choice_vote>=10 and choice_vote<=50:
                rating = "warm"
            else:
                rating="normal"
            ratings.append(rating)
            
         
    print(ratings)

    return render(request, "home.html" , {'latest_question_list':latest_question_list , 'rating':rating})

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

    