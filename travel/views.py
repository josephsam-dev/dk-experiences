from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

import requests
import qrcode
import os

from .models import TravelPackage, Booking, BlogPost, PartnershipApplication, Ticket


# =========================
# TRAVEL
# =========================
def travel_page(request):
    packages = TravelPackage.objects.all()
    return render(request, "travel.html", {"packages": packages})


def travel_detail(request, id):
    package = get_object_or_404(TravelPackage, id=id)
    return render(request, "travel_detail.html", {"package": package})


# =========================
# BLOG
# =========================
def blog_page(request):
    posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "blog.html", {"posts": posts})


def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, "blog_detail.html", {"post": post})


# =========================
# PARTNERSHIP
# =========================
def partnership(request):
    if request.method == "POST":
        PartnershipApplication.objects.create(
            company_name=request.POST.get("company_name"),
            contact_person=request.POST.get("contact_person"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            partnership_type=request.POST.get("partnership_type"),
            message=request.POST.get("message")
        )
        messages.success(request, "Application submitted!")
        return redirect("partnership")

    return render(request, "travel/partnership.html")


# =========================
# PAYMENT VERIFY
# =========================
def verify_payment(request):
    reference = request.GET.get("reference")

    if not reference:
        return HttpResponse("No reference provided")

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}

    response = requests.get(url, headers=headers)
    result = response.json()

    if result["data"]["status"] == "success":
        data = request.session.get("ticket_data")

        Ticket.objects.create(
            ticket_id=reference,
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            ticket_type=data["ticket_type"],
            payment_status="paid"
        )

        # QR
        verify_url = f"http://127.0.0.1:8000/verify-ticket/{reference}/"
        img = qrcode.make(verify_url)
        path = os.path.join(settings.MEDIA_ROOT, f"ticket_{reference}.png")
        img.save(path)

        send_mail(
            "Ticket Confirmation",
            f"Hello {data['name']}, your ticket is confirmed.",
            settings.EMAIL_HOST_USER,
            [data["email"]],
        )

        return redirect(f"/booking-success/?reference={reference}")

    return HttpResponse("Payment failed")


# =========================
# SUCCESS
# =========================
def booking_success(request):
    reference = request.GET.get("reference")
    return render(request, "booking_success.html", {"reference": reference})


# =========================
# VERIFY TICKET
# =========================
def verify_ticket(request, reference):
    status = "valid" if Ticket.objects.filter(ticket_id=reference).exists() else "invalid"
    return render(request, "verify_ticket.html", {"reference": reference, "status": status})


# =========================
# DOWNLOAD
# =========================
def download_ticket(request):
    reference = request.GET.get("reference")
    file_path = os.path.join(settings.MEDIA_ROOT, f"ticket_{reference}.png")

    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), as_attachment=True)

    return HttpResponse("Ticket not found")


# =========================
# BUY TICKET
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
            "amount": int(float(ticket.amount) * 100)
        }

        response = requests.post(url, json=data, headers=headers)
        res_data = response.json()

        if res_data.get("status"):
            return redirect(res_data["data"]["authorization_url"])

        return HttpResponse("Payment failed")

    return render(request, "buy_ticket.html", {"ticket": ticket})


from events.models import Event

def event_tickets(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = event.tickets.all()

    return render(request, "event_tickets.html", {
        "event": event,
        "tickets": tickets
    })