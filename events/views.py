
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
=======
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse
from .models import Ticket


# ✅ EVENTS PAGE
def events(request):
    return render(request, "events.html")


# ✅ BUY TICKET (PAYSTACK)
def buy_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if request.method == "POST":
        email = request.POST.get("email")

        url = "https://api.paystack.co/transaction/initialize"

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": email,
            "amount": int(ticket.price) * 100,
            "callback_url": "http://127.0.0.1:8000/events/payment-success/?ticket_id=" + str(ticket.id)
        }

        response = requests.post(url, json=data, headers=headers)

        # 🔥 DEBUG OUTPUT
        print("STATUS CODE:", response.status_code)
        print("RESPONSE TEXT:", response.text)

        res_data = response.json()

        if res_data.get("status"):
            return redirect(res_data["data"]["authorization_url"])
        else:
            return HttpResponse("Payment failed ❌")

    return render(request, "buy_ticket.html", {"ticket": ticket})


# ✅ EVENT DETAIL PAGE
def event_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, "event_detail.html", {"ticket": ticket})


# ✅ PAYMENT SUCCESS PAGE (FIXED INDENTATION)
def payment_success(request):
    reference = request.GET.get("reference")
    ticket_id = request.GET.get("ticket_id")

    if not reference:
        return HttpResponse("No payment reference ❌")

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(url, headers=headers)
    res_data = response.json()

    print("VERIFY RESPONSE:", res_data)

    if res_data.get("status") and res_data["data"]["status"] == "success":
        ticket = get_object_or_404(Ticket, id=ticket_id)

        # ✅ SAVE PAYMENT
        ticket.payment_reference = reference
        ticket.paid = True
        ticket.save()

        return render(request, "booking_success.html", {"ticket": ticket})

    return HttpResponse("Payment verification failed ❌")


from django.shortcuts import render

def blog(request):
    posts = []  # 🔥 temporary (no database yet)

    return render(request, "blog.html", {
        "posts": posts
    })

