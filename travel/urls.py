from django.urls import path
from . import views

urlpatterns = [
    path("", views.travel_page, name="travel"),

    path("event/<int:event_id>/tickets/", views.event_tickets, name="event_tickets"),

    path("buy-ticket/<int:id>/", views.buy_ticket, name="buy_ticket"),

    path("payment-success/", views.booking_success, name="payment_success"),

    path("partnership/", views.partnership, name="partnership"),

    # 🔥 ADD THIS
    path("package/<int:id>/", views.travel_detail, name="travel_detail"),
]