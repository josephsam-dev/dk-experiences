from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages

import requests
import qrcode
import os


from .models import TravelPackage, Booking, BlogPost, PartnershipApplication, Ticket

# TRAVEL PACKAGES PAGE
def travel_page(request):
    packages = TravelPackage.objects.all()
    return render(request, "travel.html", {"packages": packages})


def travel_detail(request, id):
    package = get_object_or_404(TravelPackage, id=id)
    return render(request, "travel_detail.html", {"package": package})


def book_travel(request, id):
    package = get_object_or_404(TravelPackage, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        travelers = request.POST.get("travelers")
        travel_date = request.POST.get("travel_date")

        booking = Booking.objects.create(
            package=package,
            name=name,
            email=email,
            phone=phone,
            travelers=travelers,
            travel_date=travel_date
        )

        return render(request, "booking_success.html", {"booking": booking})

    return render(request, "booking.html", {"package": package})


# BLOG PAGE
def blog_page(request):
    posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "blog.html", {"posts": posts})


# BLOG DETAIL PAGE
def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, "blog_detail.html", {"post": post})


# CONTACT PAGE
def contact(request):
    return render(request, "contact.html")

# PARTNERSHIP PAGE
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

def partnership(request):

    if request.method == "POST":
        company_name = request.POST.get("company_name")
        contact_person = request.POST.get("contact_person")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        partnership_type = request.POST.get("partnership_type")
        message = request.POST.get("message")

        PartnershipApplication.objects.create(
            company_name=company_name,
            contact_person=contact_person,
            email=email,
            phone=phone,
            partnership_type=partnership_type,
            message=message
        )

        messages.success(request, "Partnership application submitted successfully!")

        return redirect("partnership")

    return render(request, "travel/partnership.html")


from .models import Ticket

from django.conf import settings



def verify_payment(request):

    reference = request.GET.get("reference")

    if not reference:
        return HttpResponse("No reference provided")

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    if result["data"]["status"] == "success":

        data = request.session.get("ticket_data")

        ticket = Ticket.objects.create(
            ticket_id=reference,
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            ticket_type=data["ticket_type"],
            payment_status="paid"
        )

        # 🎯 GENERATE QR
        verify_url = f"http://127.0.0.1:8000/verify-ticket/{reference}/"
        img = qrcode.make(verify_url)
        path = os.path.join(settings.MEDIA_ROOT, f"ticket_{reference}.png")
        img.save(path)
        

        return redirect(f"/booking-success/?reference={reference}")

    return HttpResponse("Payment verification failed")



import requests
import qrcode
from django.http import HttpResponse
from django.conf import settings
from .models import Ticket


from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
import requests
import qrcode
import os
from .models import Ticket


def verify_payment(request):

    reference = request.GET.get("reference")

    if not reference:
        return HttpResponse("No reference provided")

    # Verify payment from Paystack
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    # ✅ If payment is successful
    if result["data"]["status"] == "success":

        data = request.session.get("ticket_data")

        # Create ticket
        Ticket.objects.create(
            ticket_id=reference,
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            ticket_type=data["ticket_type"],
            payment_status="paid"
        )

        # Generate QR
        verify_url = f"http://127.0.0.1:8000/verify-ticket/{reference}/"
        img = qrcode.make(verify_url)
        path = os.path.join(settings.MEDIA_ROOT, f"ticket_{reference}.png")
        img.save(path)

        # Send email (simple first)
        send_mail(
            "Ticket Confirmation",
            f"Hello {data['name']}, your ticket is confirmed. Ticket ID: {reference}",
            settings.EMAIL_HOST_USER,
            [data["email"]],
        )

        return redirect(f"/booking-success/?reference={reference}")

    # ❌ If payment fails
    return HttpResponse("Payment verification failed")
def booking_success(request):
    reference = request.GET.get("reference")
    return render(request, "booking_success.html", {"reference": reference})


def verify_ticket(request, reference):

    try:
        ticket = Ticket.objects.get(ticket_id=reference)

        return HttpResponse("""
        <h1 style='color:green;text-align:center;margin-top:100px;'>
        ✅ VALID TICKET
        </h1>
        """)

    except Ticket.DoesNotExist:

        return HttpResponse("""
        <h1 style='color:red;text-align:center;margin-top:100px;'>
        ❌ INVALID TICKET
        </h1>
        """)

 
from django.http import FileResponse, HttpResponse
import os

def download_ticket(request):
    reference = request.GET.get("reference")

    file_path = os.path.join(settings.MEDIA_ROOT, f"ticket_{reference}.png")

    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), as_attachment=True)

    return HttpResponse("Ticket not found")



def verify_ticket(request, reference):
    from .models import Ticket

    try:
        ticket = Ticket.objects.get(ticket_id=reference)
        status = "valid"
    except Ticket.DoesNotExist:
        status = "invalid"

    return render(request, "verify_ticket.html", {
        "reference": reference,
        "status": status
    })

from django.conf import settings
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Ticket  # or your model name

def buy_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    return render(request, "travel/buy_ticket.html", {
        "ticket": ticket,
        "PAYSTACK_PUBLIC_KEY": settings.PAYSTACK_PUBLIC_KEY
    })



    from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@gmail.com", "admin123")
        return HttpResponse("Admin created")
    return HttpResponse("Admin already exists")