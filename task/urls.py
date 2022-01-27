from django.urls import path
from task.views import hello

urlpatterns = [
    path('hello/', hello, name='hello'),
]
