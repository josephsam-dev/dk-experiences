from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD

    path("test/", views.test_page),  # 👈 ADD THIS LINE HERE (VERY TOP)

    path("", views.travel_page, name="travel"),

    path("buy-ticket/<int:id>/", views.buy_ticket, name="buy_ticket"),

    path("verify-payment/", views.verify_payment, name="verify_payment"),

    path("booking-success/", views.booking_success, name="booking_success"),

    path("download-ticket/", views.download_ticket, name="download_ticket"),

    path("verify-ticket/<str:reference>/", views.verify_ticket, name="verify_ticket"),

    # KEEP THIS LAST
    path("<int:id>/", views.travel_detail, name="travel_detail"),
=======
    path("", views.travel_page, name="travel"),

    path("event/<int:event_id>/tickets/", views.event_tickets, name="event_tickets"),

    path("buy-ticket/<int:id>/", views.buy_ticket, name="buy_ticket"),

    path("payment-success/", views.booking_success, name="payment_success"),

    path("partnership/", views.partnership, name="partnership"),

    # 🔥 ADD THIS
    path("package/<int:id>/", views.travel_detail, name="travel_detail"),
>>>>>>> 2ac0cf1 (fresh clean commit without secrets)
]