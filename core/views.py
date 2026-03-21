from django.shortcuts import render
from events.models import Event

def home(request):
    return render(request, 'home.html')

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})