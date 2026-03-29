from django.urls import path
from . import views

urlpatterns = [

    path("test/", views.test_page),  # 👈 ADD THIS LINE HERE (VERY TOP)

    path("", views.travel_page, name="travel"),

    path("buy-ticket/<int:id>/", views.buy_ticket, name="buy_ticket"),

    path("verify-payment/", views.verify_payment, name="verify_payment"),

    path("booking-success/", views.booking_success, name="booking_success"),

    path("download-ticket/", views.download_ticket, name="download_ticket"),

    path("verify-ticket/<str:reference>/", views.verify_ticket, name="verify_ticket"),

    # KEEP THIS LAST
    path("<int:id>/", views.travel_detail, name="travel_detail"),
]