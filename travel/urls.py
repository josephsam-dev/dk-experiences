from django.urls import path
from . import views

urlpatterns = [

    # 🔥 PUT BLOG FIRST
    path("blog/", views.blog, name="blog"),

    path("", views.travel_page, name="travel"),

    path("package/<int:id>/", views.travel_detail, name="travel_detail"),

    path("buy-ticket/", views.buy_ticket, name="buy_ticket"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path("payment-success/", views.booking_success, name="payment_success"),
    path("booking-success/", views.booking_success, name="booking_success"),

    path("download-ticket/", views.download_ticket, name="download_ticket"),
    path("verify-ticket/<str:reference>/", views.verify_ticket, name="verify_ticket"),

    path("partnership/", views.partnership, name="partnership"),
    path("buy-ticket/<int:event_id>/", views.buy_ticket, name="travel_buy_ticket"),

    # ❗ KEEP THIS LAST ALWAYS
    path("<int:id>/", views.travel_detail, name="travel_detail"),
]