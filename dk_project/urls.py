from django.http import HttpResponse
from django.urls import path

def crash_test(request):
    1 / 0  # force error

urlpatterns = [
    path('', crash_test),
]