from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.travel_detail, name="travel_detail"),
    path("", views.travel_page, name="travel"),
    path("book/<int:id>/", views.book_travel, name="book_travel"),
    path("blog/", views.blog_page, name="blog"),
    path("blog/<int:id>/", views.blog_detail, name="blog_detail"),

    path("contact/", views.contact, name="contact"),   # ADD THIS

    path("partnership/", views.partnership, name="partnership"),
    path("buy-ticket/<int:id>/", views.buy_ticket, name="buy_ticket"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path("booking-success/", views.booking_success, name="booking_success"),
    path("download-ticket/", views.download_ticket, name="download_ticket"),
    path('verify-ticket/<str:reference>/', views.verify_ticket, name='verify_ticket'),
    path("create-admin/", views.create_admin),
]