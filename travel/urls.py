from django.urls import path
from . import views

urlpatterns = [

    # MAIN PAGE
    path("", views.travel_page, name="travel"),

    # TRAVEL DETAILS
    path("package/<int:id>/", views.travel_detail, name="travel_detail"),

    # ✅ BOOKING / PAYMENT (FIXED PARAMETER NAME)
    path("buy-ticket/<int:ticket_id>/", views.buy_ticket, name="buy_ticket"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path("payment-success/", views.booking_success, name="payment_success"),
    path("booking-success/", views.booking_success, name="booking_success"),

    # TICKETS
    path("download-ticket/", views.download_ticket, name="download_ticket"),
    path("verify-ticket/<str:reference>/", views.verify_ticket, name="verify_ticket"),

    # PARTNERSHIP
    path("partnership/", views.partnership, name="partnership"),
]