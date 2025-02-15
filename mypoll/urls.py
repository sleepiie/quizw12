from django.urls import path
from mypoll import views

app_name = "mypoll"
urlpatterns = [
    path("", views.home_page, name="homepage"),
    path("vote/<int:question_id>/" , views.vote , name="vote"),
    path('results/<int:question_id>/', views.results, name='results'),
]