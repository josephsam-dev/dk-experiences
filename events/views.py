from .models import Event, Ticket
from django.shortcuts import render, get_object_or_404
from .models import Event


def events_page(request):
    events = Event.objects.all()
    return render(request, "events.html", {"events": events})


def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, "event_detail.html", {"event": event})

def buy_ticket(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        category = request.POST.get("category")
        quantity = request.POST.get("quantity")

        event = Event.objects.first()

        Ticket.objects.create(
            event=event,
            category=category,
            price=event.price,
            buyer_name=name,
            buyer_email=email,
            quantity=quantity
        )

        return render(request, "booking_success.html")

    return render(request, "buy_ticket.html")