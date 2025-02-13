from django.urls import path
from mypoll import views

app_name = "mypoll"
urlpatterns = [
    path("", views.home_page, name="homepage"),
]