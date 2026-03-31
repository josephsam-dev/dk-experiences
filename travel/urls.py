from django.urls import path
from . import views

urlpatterns = [

    # TEST
    path("test/", views.test_page, name="test"),

    # MAIN PAGE
    path("", views.travel_page, name="travel"),

    # TRAVEL DETAILS
    path("package/<int:id>/", views.travel_detail, name="travel_detail"),

    # BOOKING / PAYMENT
    path("buy-ticket/<int:id>/", views.buy_ticket, name="buy_ticket"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path("payment-success/", views.booking_success, name="payment_success"),
    path("booking-success/", views.booking_success, name="booking_success"),

    # TICKETS
    path("download-ticket/", views.download_ticket, name="download_ticket"),
    path("verify-ticket/<str:reference>/", views.verify_ticket, name="verify_ticket"),

    # EVENTS
    path("event/<int:event_id>/tickets/", views.event_tickets, name="event_tickets"),

    # PARTNERSHIP
    path("partnership/", views.partnership, name="partnership"),
]