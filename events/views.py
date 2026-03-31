from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
import requests

from .models import Event, Ticket


# =========================
# EVENTS PAGE
# =========================
def events_page(request):
    events = Event.objects.all()
    return render(request, "events.html", {"events": events})


# =========================
# EVENT DETAIL
# =========================
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, "event_detail.html", {"event": event})


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


# =========================
# BLOG (TEMP)
# =========================
def blog(request):
    posts = []
    return render(request, "blog.html", {"posts": posts})