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
def blog(request):
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
import qrcode
from io import BytesIO
import base64

def booking_success(request):
    reference = request.GET.get("reference")
    ticket = Ticket.objects.filter(reference=reference).first()

    qr_image = None

    if ticket:
        verify_url = f"https://dkexperience.com.ng/events/verify-ticket/{ticket.reference}/"

        qr = qrcode.make(verify_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        qr_image = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "travel_booking_success.html", {
        "ticket": ticket,
        "qr_image": qr_image
    })

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

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from events.models import Event, Ticket


# =========================
# BUY TICKET (FINAL)
# =========================
from .models import TravelPackage, Ticket

def buy_ticket(request, event_id):
    package = get_object_or_404(TravelPackage, id=event_id)

    tickets = Ticket.objects.all()  # 👈 FIX

    return render(request, "travel/buy_ticket.html", {
        "package": package,
        "tickets": tickets,
        "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY
    })


from django.shortcuts import render, get_object_or_404
from .models import TravelPackage

def travel_page(request):
    packages = TravelPackage.objects.all()
    return render(request, "travel.html", {"packages": packages})


def travel_detail(request, id):
    trip = get_object_or_404(TravelPackage, id=id)
    return render(request, "travel_detail.html", {"package": trip})