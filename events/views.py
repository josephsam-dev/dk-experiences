import json
import uuid
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from .models import Event
from core.models import Ticket
# =========================
# EVENTS PAGE
# =========================
def events_page(request):
    events = Event.objects.all()
    return render(request, "events.html", {"events": events})


# =========================
# EVENT DETAIL
# =========================
from django.shortcuts import render, get_object_or_404
from .models import Event
from core.models import Ticket

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)

    tickets = Ticket.objects.filter(event=event)

    return render(request, "events/event_detail.html", {
        "event": event,
        "tickets": tickets
    })

# =========================
# BUY TICKET (PAYSTACK)
# =========================
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
            "callback_url": f"https://dkexperience.com.ng/events/payment-success/?ticket_id={ticket.id}"
        }

        response = requests.post(url, json=data, headers=headers)
        res_data = response.json()

        if res_data.get("status"):
            return redirect(res_data["data"]["authorization_url"])
        else:
            return HttpResponse("Payment failed ❌")

    return render(request, "buy_ticket.html", {"ticket": ticket})


# =========================
# PAYMENT SUCCESS
# =========================
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

    if res_data.get("status") and res_data["data"]["status"] == "success":
        ticket = get_object_or_404(Ticket, id=ticket_id)

        ticket.payment_reference = reference
        ticket.paid = True
        ticket.save()

        return render(request, "booking_success.html", {"ticket": ticket})

    return HttpResponse("Payment verification failed ❌")


import uuid
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from core.models import Ticket


from django.http import HttpResponse

def create_ticket(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        tickets = request.POST.get("tickets")
        total = int(request.POST.get("total") or 0)

        reference = str(uuid.uuid4())

        ticket = Ticket.objects.create(
            email=email,
            phone=phone,
            ticket_data=tickets,
            total_amount=total,
            reference=reference
        )

        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": email,
            "amount": total * 100,
            "reference": reference,
            "callback_url": f"https://dkexperience.com.ng/payment-success/?reference={reference}&ticket_id={ticket.id}"
        }

        response = requests.post(url, json=data, headers=headers)
        res_data = response.json()

        # ✅ HANDLE ERROR (THIS IS THE FIX)
        if not res_data.get("status"):
            return HttpResponse(f"Paystack Error: {res_data}")

        # ✅ SUCCESS
        return redirect(res_data["data"]["authorization_url"])

    return HttpResponse("Invalid request")