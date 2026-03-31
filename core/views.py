<<<<<<< HEAD
from django.shortcuts import render
from events.models import Event

def home(request):
    return render(request, 'home.html')

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})
=======
from django.shortcuts import render, get_object_or_404
from events.models import Event
from travel.models import BlogPost


def home(request):
    try:
        event = Event.objects.first()
    except:
        event = None

    return render(request, 'home.html', {
        'event': event
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
>>>>>>> 2ac0cf1 (fresh clean commit without secrets)
