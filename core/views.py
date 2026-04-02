
from django.shortcuts import render
from events.models import Event

def home(request):
    return render(request, 'home.html')

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

from django.shortcuts import render, get_object_or_404
from events.models import Event
from travel.models import BlogPost


from events.models import Event

def home(request):
    events = Event.objects.all().order_by('-date')

    return render(request, 'home.html', {
        'events': events
    })


def contact(request):
    return render(request, "contact.html")


def blog(request):
    posts = BlogPost.objects.all().order_by('-id')
    return render(request, "blog.html", {
        "posts": posts
    })


def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, "blog_detail.html", {
        "post": post
    })

