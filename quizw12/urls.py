from django.contrib import admin
from django.urls import include, path

app_name = "mypoll"
urlpatterns = [
    path('', include('mypoll.urls', namespace='mypoll')),
    path('admin/', admin.site.urls),
]
