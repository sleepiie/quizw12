from django.shortcuts import render
from mypoll.models import Question , Choice

def home_page(request):
    return render(request, "home.html")
