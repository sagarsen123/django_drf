from home.views import *
from django.urls import path


urlpatterns = [
    path('index/', index),
    path('login/', login),
    path('person/', people)
]
